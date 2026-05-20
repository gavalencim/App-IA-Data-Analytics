import pandas as pd


class CSVService:

    @staticmethod
    def load_csv(file):

        df = pd.read_csv(file)

        return df

    @staticmethod
    def get_basic_info(df):

        return {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "column_names": list(df.columns),
            "missing_values": df.isnull().sum().to_dict()
        }

    @staticmethod
    def get_preview(df, rows=5):

        return df.head(rows).to_html(
            classes="table table-striped",
            index=False
        )
    
    @staticmethod
    def detect_column_types(df):

        numeric_columns = list(
            df.select_dtypes(include=['number']).columns
        )

        categorical_columns = list(
            df.select_dtypes(
                include=['object', 'category']
            ).columns
        )

        return {
            "numeric": numeric_columns,
            "categorical": categorical_columns
        }