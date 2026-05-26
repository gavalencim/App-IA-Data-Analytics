import json
#from google import genai
#from google.genai import types
from django.conf import settings
from openai import OpenAI


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=settings.NVIDIA_API_KEY
)

# MODEL = "gemini-2.5-flash-lite"
MODEL = "meta/llama-3.3-70b-instruct"


class DatasetAIService:

    # ==========================================
    # BUILD DATASET PROFILE
    # ==========================================

    @staticmethod
    def build_dataset_profile(df):

        profile = []

        for column in df.columns:

            column_info = {
                "column_name": column,
                "dtype": str(df[column].dtype),
                "n_unique": int(df[column].nunique()),
                "sample_values": (
                    df[column]
                    .dropna()
                    .astype(str)
                    .head(50)
                    .tolist()
                )
            }

            # ======================================
            # INCLUDE POSSIBLE VALUES
            # FOR CATEGORICAL COLUMNS
            # ======================================

            if str(df[column].dtype) in [
                "object",
                "str"
            ]:

                possible_values = (
                    df[column]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                column_info["possible_values"] = (
                    possible_values[:30]
                )

            profile.append(column_info)

        return profile

    # ==========================================
    # ANALYZE DATASET
    # ==========================================

    @staticmethod
    def analyze_dataset(
        profile,
        analysis_goal,
        selected_columns
    ):

        prompt = f"""
You are a senior data analyst and
data visualization expert.

The user wants to analyze:
{analysis_goal}

The user selected these columns:
{selected_columns}

Your task:
Recommend the MOST insightful and
useful visualizations for the dataset.

IMPORTANT:

Do NOT only analyze columns individually.

You MUST identify:
- numerical columns
- categorical columns
- datetime columns
- meaningful relationships

You should prioritize:
- trends
- comparisons
- distributions
- correlations
- aggregations
- business insights

================================================
SUPPORTED CHART TYPES
================================================

1. histogram
Purpose:
- numerical distributions

Required:
- x

Example:
{{
    "chart_type": "histogram",
    "x": "salary",
    "title": "Salary distribution"
}}

------------------------------------------------

2. countplot
Purpose:
- frequency of categories

Required:
- x

Example:
{{
    "chart_type": "countplot",
    "x": "gender",
    "title": "Gender distribution"
}}

------------------------------------------------

3. barplot
Purpose:
- compare numerical values grouped
by categories

Required:
- x
- y
- aggregation

Aggregation options:
- mean
- sum
- median
- count

Examples:
- average salary by gender
- total sales by seller
- total victims by department

Example:
{{
    "chart_type": "barplot",
    "x": "seller",
    "y": "sales",
    "aggregation": "sum",
    "title": "Total sales by seller"
}}

IMPORTANT:
- x MUST be categorical
- y MUST be numerical

------------------------------------------------

4. scatterplot
Purpose:
- relationship between two numerical variables

Required:
- x
- y

Example:
{{
    "chart_type": "scatterplot",
    "x": "age",
    "y": "salary",
    "title": "Age vs salary"
}}

------------------------------------------------

5. lineplot
Purpose:
- trends over time

Required:
- x
- y

Example:
{{
    "chart_type": "lineplot",
    "x": "date",
    "y": "sales",
    "title": "Sales over time"
}}

IMPORTANT:
- x should preferably be datetime

------------------------------------------------

6. heatmap
Purpose:
- numerical correlations

Required:
- no x/y required

Example:
{{
    "chart_type": "heatmap",
    "title": "Correlation matrix"
}}

------------------------------------------------

7. boxplot
Purpose:
- distribution comparison across categories

Required:
- x
- y

Example:
{{
    "chart_type": "boxplot",
    "x": "department",
    "y": "salary",
    "title": "Salary distribution by department"
}}

------------------------------------------------

8. violinplot
Purpose:
- advanced distribution comparison

Required:
- x
- y

Example:
{{
    "chart_type": "violinplot",
    "x": "gender",
    "y": "salary",
    "title": "Salary distribution by gender"
}}

================================================
IMPORTANT VISUALIZATION RULES
================================================

1. Prioritize the MOST useful visualizations.

2. Avoid repetitive charts.

3. Maximum 50 charts.

4. Prefer meaningful relationships.

5. Use aggregation charts when possible.

6. Do NOT create multiple charts showing
the exact same information.

7. If the dataset contains many numerical
columns, include at least:
- one correlation heatmap
- one scatterplot if meaningful

8. If categorical + numerical relationships
exist, prioritize barplots and boxplots.

================================================
CRITICAL DATA INTEGRITY RULES
================================================

1. NEVER invent semantic meanings.

2. ONLY use the exact information
present in the dataset profile.

3. Do NOT assume abbreviations meanings.

Examples:
- "F" and "M" do NOT necessarily
mean female/male
- "CA" does NOT necessarily mean California
- "A" does NOT imply category A

4. Base all analysis STRICTLY on:
- column names
- data types
- sample values
- unique values count
- possible values

5. If meaning is unclear,
treat as generic data.

6. NEVER hallucinate business contexts.

7. NEVER invent interpretations.

8. NEVER create fake insights.

9. ONLY use EXISTING columns.

10. NEVER create columns that do not exist.

================================================
RETURN FORMAT
================================================

Return ONLY valid JSON.

Example:

[
    {{
        "chart_type": "histogram",
        "x": "salary",
        "title": "Salary distribution"
    }},

    {{
        "chart_type": "countplot",
        "x": "department",
        "title": "Department frequency"
    }},

    {{
        "chart_type": "barplot",
        "x": "seller",
        "y": "sales",
        "aggregation": "sum",
        "title": "Total sales by seller"
    }},

    {{
        "chart_type": "scatterplot",
        "x": "age",
        "y": "salary",
        "title": "Age vs salary"
    }},

    {{
        "chart_type": "heatmap",
        "title": "Correlation matrix"
    }}
]

================================================
DATASET PROFILE
================================================

{json.dumps(profile, indent=2)}
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        text = response.choices[0].message.content

        print("\n========== RAW AI RESPONSE ==========")
        print(text)

        clean_text = (
            text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        # ======================================
        # EXTRACT JSON ARRAY SAFELY
        # ======================================

        start = clean_text.find("[")
        end = clean_text.rfind("]") + 1

        if start == -1 or end == 0:

            raise Exception(
                f"Model did not return valid JSON.\n\nResponse:\n{text}"
            )

        json_text = clean_text[start:end]

        print("\n========== CLEAN JSON ==========")
        print(json_text)

        return json.loads(json_text)