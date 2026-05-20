import json
from google import genai
from google.genai import types
from django.conf import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

MODEL = "gemini-2.5-flash-lite"


class DatasetAIService:

    @staticmethod
    def build_dataset_profile(df):

        profile = []

        for column in df.columns:

            profile.append({
                "column_name": column,
                "dtype": str(df[column].dtype),
                "n_unique": int(df[column].nunique()),
                "sample_values": (
                    df[column]
                    .dropna()
                    .astype(str)
                    .head(5)
                    .tolist()
                )
            })

        return profile

    @staticmethod
    def analyze_dataset(profile, analysis_goal, selected_columns):

        prompt = f"""
You are an expert data analyst.

The user wants to analyze:
{analysis_goal}

The user selected these columns:
{selected_columns}

Your task is to recommend INSIGHTFUL visualizations.

IMPORTANT:
Do NOT only analyze columns individually.

You should also analyze RELATIONSHIPS between variables.

You MUST identify:
- numerical columns
- categorical columns
- meaningful relationships

Recommended visualizations can include:

1. histogram
- For numerical distributions

2. categorical_frequency
- For category counts

3. bar_aggregation
- For comparing a numerical variable grouped by a categorical variable

Examples:
- average salary by gender
- total sales by seller
- average score by school

For aggregation charts:
- x_column MUST be categorical
- y_column MUST be numerical
- aggregation can be:
    - mean
    - sum
    - median

IMPORTANT:
Prioritize the MOST useful visualizations.
Avoid repetitive charts.
Maximum 10 charts.

Return ONLY valid JSON.

Example:

[
    {{
        "chart_type": "histogram",
        "column": "salary"
    }},

    {{
        "chart_type": "categorical_frequency",
        "column": "gender"
    }},

    {{
        "chart_type": "bar_aggregation",
        "x_column": "gender",
        "y_column": "salary",
        "aggregation": "mean"
    }}
]

Dataset profile:
{json.dumps(profile, indent=2)}

CRITICAL RULES:

1. NEVER invent semantic meanings for values.

2. ONLY use the exact information present in the dataset profile.

3. Do NOT assume abbreviations meanings.

Examples:
- "F" and "M" do NOT necessarily mean female/male
- "CA" does NOT necessarily mean California
- "A" does NOT imply category A

4. Base all analysis strictly on:
- column names
- data types
- sample values
- unique values count

5. If the meaning of a column is unclear,
treat it as generic categorical data.

6. NEVER hallucinate domain interpretations.

7. Do NOT create fake business meanings or contexts.
"""

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

        return json.loads(clean_text)