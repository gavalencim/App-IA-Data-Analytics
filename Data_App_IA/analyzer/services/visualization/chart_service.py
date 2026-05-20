import os
import uuid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.conf import settings


class ChartService:


    @staticmethod
    def save_chart():

        filename = f"{uuid.uuid4()}.png"

        relative_path = os.path.join(
            "charts",
            filename
        )

        full_path = os.path.join(
            settings.MEDIA_ROOT,
            relative_path
        )

        os.makedirs(
            os.path.dirname(full_path),
            exist_ok=True
        )

        plt.tight_layout()
        plt.savefig(full_path)
        plt.close()

        return f"/media/{relative_path.replace('\\', '/')}"


    @staticmethod
    def generate_histogram(df, column):

        plt.figure(figsize=(8,5))
        ax = df[column].dropna().hist(bins=20)
        df[column].hist()
        plt.title(f"Distribución de {column}", fontweihgt='bold')
        plt.xlabel(column)
        plt.ylabel("Frecuencia")

        ax.xaxis.set_major_formatter(
            plt.FuncFormatter(
                lambda x, _: f"{x:,.0f}"
            )
        )

        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(
                lambda y, _: f"{y:,.0f}"
            )
        )

        return ChartService.save_chart()


    @staticmethod
    def generate_bar_chart(df, column):

        value_counts = (
            df[column]
            .astype(str)
            .value_counts()
            .head(10)
        )

        plt.figure(figsize=(9,5))
        value_counts.plot(kind='bar')
        ax = value_counts.plot(kind='bar')
        plt.title(f"Frecuencia de {column}", fontweight="bold")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=45, ha="right")
        plt.grid(axis='y',alpha=0.3)

        for i, value in enumerate(value_counts):

            ax.text(
                i,
                value + 0.5,
                f"{value:,}",
                ha='center',
                fontsize=10
            )

        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(
                lambda y, _: f"{y:,.0f}"
            )
        )

        return ChartService.save_chart()
    
    @staticmethod
    def generate_aggregation_bar_chart(
        df,
        x_column,
        y_column,
        aggregation="mean"):

        if aggregation == "mean":

            grouped = (
                df.groupby(x_column)[y_column]
                .mean()
            )

        elif aggregation == "sum":

            grouped = (
                df.groupby(x_column)[y_column]
                .sum()
            )

        elif aggregation == "median":

            grouped = (
                df.groupby(x_column)[y_column]
                .median()
            )

        else:

            grouped = (
                df.groupby(x_column)[y_column]
                .mean()
            )

        grouped = grouped.sort_values(ascending=False).head(10)    
        plt.figure(figsize=(10,6))
        ax = grouped.plot(kind="bar")
        grouped.plot(kind="bar")
        plt.title(
            f"{aggregation} de {y_column} por {x_column}", fontweight="bold"
        )
        plt.ylabel(y_column)
        plt.xlabel(x_column)
        plt.xticks(rotation=45, ha="right")
        plt.grid(axis='y',alpha=0.3)

        for i, value in enumerate(grouped):

            ax.text(
                i,
                value,
                f"{value:,.0f}",
                ha='center',
                va='bottom',
                fontsize=10
            )

        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(
                lambda y, _: f"{y:,.0f}"
            )
        )

        return ChartService.save_chart()

    @staticmethod
    def generate_charts_from_ai(df, ai_analysis):

        chart_paths = []

        print(ai_analysis)

        for item in ai_analysis:

            try:

                chart_type = (
                    item["chart_type"]
                    .lower()
                    .strip()
                )

                print(
                    f"Generating: {chart_type}"
                )

                # ==================================
                # HISTOGRAM
                # ==================================

                if chart_type == "histogram":

                    column = item["column"]

                    chart = (
                        ChartService
                        .generate_histogram(
                            df,
                            column
                        )
                    )

                    chart_paths.append(chart)

                # ==================================
                # CATEGORICAL FREQUENCY
                # ==================================

                elif (
                    chart_type
                    == "categorical_frequency"
                ):

                    column = item["column"]

                    chart = (
                        ChartService
                        .generate_bar_chart(
                            df,
                            column
                        )
                    )

                    chart_paths.append(chart)

                # ==================================
                # AGGREGATION BAR
                # ==================================

                elif (
                    chart_type
                    == "bar_aggregation"
                ):

                    x_column = item["x_column"]

                    y_column = item["y_column"]

                    aggregation = item.get(
                        "aggregation",
                        "mean"
                    )

                    chart = (
                        ChartService
                        .generate_aggregation_bar_chart(
                            df,
                            x_column,
                            y_column,
                            aggregation
                        )
                    )

                    chart_paths.append(chart)

                else:

                    print(
                        f"Unsupported chart type: "
                        f"{chart_type}"
                    )

            except Exception as e:

                import traceback

                print(
                    "\nERROR GENERATING CHART\n"
                )

                traceback.print_exc()

        return chart_paths
