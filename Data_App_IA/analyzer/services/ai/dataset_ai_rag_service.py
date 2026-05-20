import json
import pandas as pd
from google import genai
from google.genai import types
from django.conf import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

MODEL = "gemini-2.5-flash-lite"

class DatasetRAGService:

    # ==========================================
    # BUILD DATASET METADATA
    # ==========================================

    @staticmethod
    def build_dataset_metadata(df):

        metadata = []

        for column in df.columns:

            dtype = str(df[column].dtype)

            column_info = {
                "column_name": column,
                "dtype": dtype,
                "sample_values":
                    (
                        df[column]
                        .dropna()
                        .astype(str)
                        .head(5)
                        .tolist()
                    )
            }

            # =====================================
            # CATEGORICAL VALUES
            # =====================================

            if dtype in ["object", "str"]:

                unique_values = (
                    df[column]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )
                column_info["possible_values"] = (
                    unique_values[:50]
                )
            metadata.append(column_info)

        return metadata
    
    # ==========================================
    # SELECT RELEVANT COLUMNS
    # ==========================================

    @staticmethod
    def select_relevant_columns(
        question,
        df
    ):

        metadata = (
            DatasetRAGService
            .build_dataset_metadata(df)
        )
        prompt = f"""
You are an expert data analyst.

Your task:
Select ONLY the columns needed
to answer the user's question.

IMPORTANT RULES:

1. ONLY use existing columns.

2. NEVER invent columns.

3. Use semantic similarity.

4. Return ONLY valid JSON.

Format:

{{
    "relevant_columns":
    ["column1", "column2"]
}}

Dataset metadata:
{json.dumps(metadata, indent=2)}

User question:
{question}
"""
        print(json.dumps(metadata, indent=2))

        response = client.models.generate_content(

            model=MODEL,
            config=types.GenerateContentConfig(
                temperature=0
            ),
            contents=prompt
        )

        clean_text = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        data = json.loads(clean_text)

        return data["relevant_columns"]


    # ==========================================
    # GENERATE PANDAS QUERY
    # ==========================================

    @staticmethod
    def generate_pandas_query(
        question,
        relevant_columns,
        df
    ):

        # ======================================
        # BUILD COLUMN CONTEXT
        # ======================================

        columns_context = []

        for col in relevant_columns:

            dtype = str(df[col].dtype)

            column_info = {

                "column_name": col,
                "dtype": dtype,

                "sample_values": (
                    df[col]
                    .dropna()
                    .astype(str)
                    .head(10)
                    .tolist()
                )
            }

            # ==================================
            # ADD POSSIBLE VALUES
            # ==================================

            if dtype in ["object", "str"]:

                unique_values = (
                    df[col]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                column_info["possible_values"] = (
                    unique_values[:50]
                )

            columns_context.append(column_info)

        # ======================================
        # PROMPT
        # ======================================

        prompt = f"""
You are a pandas expert.

The dataframe name is:
df

Your task:
Generate ONLY valid pandas code
to answer the user's question.

IMPORTANT RULES:

1. Return ONLY executable pandas code.

2. DO NOT include explanations.

3. DO NOT include markdown.

4. DO NOT use imports.

5. DO NOT use print().

6. DO NOT invent columns.

7. DO NOT invent values.

8. Use ONLY values that exist
inside possible_values.

9. Values are CASE SENSITIVE.

10. The final expression MUST
return a result.

11. If the dataset contains a column
representing counts or quantities
like:
- CANTIDAD
- TOTAL
- COUNT
- CASOS
- NUMERO

and the user asks:
- how many
- total
- count
- cuantos
- cantidad

then use .sum()
instead of returning rows.

12. Only return rows if the user
explicitly asks to SEE the records.

13. You MUST perform semantic matching.

Examples:

- women -> FEMENINO
- female -> FEMENINO
- men -> MASCULINO
- antioquia -> ANTIOQUIA

Relevant columns metadata:
{json.dumps(columns_context, indent=2)}

User question:
{question}
"""

        response = client.models.generate_content(

            model=MODEL,

            config=types.GenerateContentConfig(
                temperature=0
            ),

            contents=prompt
        )

        code = (
            response.text
            .replace("```python", "")
            .replace("```", "")
            .strip()
        )

        print("\n========== GENERATED QUERY ==========")
        print(code)

        return code

    # ==========================================
    # SAFE EXECUTION
    # ==========================================

    @staticmethod
    def execute_pandas_query(
        code,
        df
    ):

        forbidden_words = [

            "import",
            "open",
            "exec",
            "eval",
            "os",
            "sys",
            "__",
            "subprocess",
            "write",
            "remove",
            "delete"
        ]

        for word in forbidden_words:

            if word in code.lower():

                raise Exception(
                    "Unsafe code detected."
                )

        safe_globals = {

            "df": df,
            "pd": pd
        }

        result = eval(
            code,
            safe_globals
        )

        return result


    # ==========================================
    # FORMAT RESULT
    # ==========================================

    @staticmethod
    def format_result(result):

        if isinstance(
            result,
            pd.DataFrame
        ):
            return result.head(20).to_string()

        elif isinstance(
            result,
            pd.Series
        ):
            return result.head(20).to_string()

        else:
            return str(result)


    # ==========================================
    # GENERATE FINAL RESPONSE
    # ==========================================

    @staticmethod
    def generate_chat_response(
        question,
        pandas_result
    ):

        prompt = f"""
You are a professional data analyst.

Your task:
Explain the result in a natural,
clear and concise way.

IMPORTANT RULES:

1. Use ONLY the provided result.

2. DO NOT invent information.

3. DO NOT hallucinate insights.

4. Be conversational and useful.

5. Use the Spanish for responses.

User question:
{question}

Pandas result:
{pandas_result}
"""

        response = client.models.generate_content(

            model=MODEL,
            config=types.GenerateContentConfig(
                temperature=0.3
            ),
            contents=prompt
        )
        return response.text


    # ==========================================
    # MAIN PIPELINE
    # ==========================================

    @staticmethod
    def ask_dataset(
        question,
        df
    ):

        # ======================================
        # STEP 1
        # SELECT COLUMNS
        # ======================================

        relevant_columns = (
            DatasetRAGService
            .select_relevant_columns(
                question,
                df
            )
        )

        if not relevant_columns:

            return {
                "answer":
                    "No relevant columns found.",
                "query": None
            }

        # ======================================
        # STEP 2
        # GENERATE QUERY
        # ======================================

        query = (
            DatasetRAGService
            .generate_pandas_query(
                question,
                relevant_columns,
                df
            )
        )

        # ======================================
        # STEP 3
        # EXECUTE QUERY
        # ======================================

        try:

            result = (
                DatasetRAGService
                .execute_pandas_query(
                    query,
                    df
                )
            )

        except Exception as e:

            return {
                "answer":
                    f"Error executing query: {e}",
                "query": query
            }

        # ======================================
        # STEP 4
        # FORMAT RESULT
        # ======================================

        formatted_result = (
            DatasetRAGService
            .format_result(result)
        )

        # ======================================
        # STEP 5
        # NATURAL LANGUAGE RESPONSE
        # ======================================

        final_answer = (
            DatasetRAGService
            .generate_chat_response(
                question,
                formatted_result
            )
        )

        return {

            "answer": final_answer,
            "query": query,
            "raw_result": formatted_result,
            "columns": relevant_columns
        }