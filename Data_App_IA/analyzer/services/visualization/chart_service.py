import os
import uuid
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from django.conf import settings
from matplotlib.ticker import FuncFormatter


# ==========================================
# SEABORN STYLE
# ==========================================

sns.set_theme(
    style="whitegrid",
    palette="deep"
)


class ChartService:


    # ==========================================
    # SAVE CHART
    # ==========================================

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

        plt.savefig(
            full_path,
            dpi=300,
            bbox_inches='tight'
        )

        plt.close()

        return f"/media/{relative_path.replace('\\', '/')}"


    # ==========================================
    # FORMAT THOUSANDS
    # ==========================================

    @staticmethod
    def thousands_formatter():

        return FuncFormatter(
            lambda x, _: f"{x:,.0f}"
        )


    # ==========================================
    # HISTOGRAM
    # ==========================================

    @staticmethod
    def generate_histogram(
        df,
        column,
        title=None
    ):

        plt.figure(figsize=(10, 6))

        ax = sns.histplot(
            data=df,
            x=column,
            bins=20,
            kde=True
        )

        plt.title(
            title or f"Distribución de {column}",
            fontsize=16,
            fontweight='bold'
        )

        plt.xlabel(column)
        plt.ylabel("Frecuencia")

        ax.xaxis.set_major_formatter(
            ChartService.thousands_formatter()
        )

        ax.yaxis.set_major_formatter(
            ChartService.thousands_formatter()
        )

        return ChartService.save_chart()


    # ==========================================
    # COUNTPLOT
    # ==========================================

    @staticmethod
    def generate_countplot(
        df,
        column,
        title=None
    ):

        top_values = (
            df[column]
            .astype(str)
            .value_counts()
            .head(10)
            .index
        )

        filtered_df = (
            df[df[column].astype(str).isin(top_values)]
        )

        plt.figure(figsize=(11, 6))

        ax = sns.countplot(
            data=filtered_df,
            x=column,
            order=top_values
        )

        plt.title(
            title or f"Frecuencia de {column}",
            fontsize=16,
            fontweight='bold'
        )

        plt.xlabel(column)
        plt.ylabel("Cantidad")

        plt.xticks(
            rotation=45,
            ha="right"
        )

        ax.yaxis.set_major_formatter(
            ChartService.thousands_formatter()
        )

        for container in ax.containers:

            ax.bar_label(
                container,
                fmt='%.0f',
                padding=3
            )

        return ChartService.save_chart()


    # ==========================================
    # BARPLOT
    # ==========================================

    @staticmethod
    def generate_barplot(
        df,
        x_column,
        y_column,
        aggregation="mean",
        title=None
    ):

        grouped = (
            df.groupby(x_column)[y_column]
            .agg(aggregation)
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        plt.figure(figsize=(12, 6))

        ax = sns.barplot(
            data=grouped,
            x=x_column,
            y=y_column
        )

        plt.title(
            title or f"{aggregation} de {y_column} por {x_column}",
            fontsize=16,
            fontweight='bold'
        )

        plt.xlabel(x_column)
        plt.ylabel(y_column)

        plt.xticks(
            rotation=45,
            ha="right"
        )

        ax.yaxis.set_major_formatter(
            ChartService.thousands_formatter()
        )

        for container in ax.containers:

            ax.bar_label(
                container,
                fmt='%.0f',
                padding=3
            )

        return ChartService.save_chart()


    # ==========================================
    # SCATTERPLOT
    # ==========================================

    @staticmethod
    def generate_scatterplot(
        df,
        x_column,
        y_column,
        title=None
    ):

        clean_df = (
            df[[x_column, y_column]]
            .dropna()
        )

        plt.figure(figsize=(10, 6))

        ax = sns.scatterplot(
            data=clean_df,
            x=x_column,
            y=y_column
        )

        plt.title(
            title or f"{x_column} vs {y_column}",
            fontsize=16,
            fontweight='bold'
        )

        plt.xlabel(x_column)
        plt.ylabel(y_column)

        return ChartService.save_chart()


    # ==========================================
    # LINEPLOT
    # ==========================================

    @staticmethod
    def generate_lineplot(
        df,
        x_column,
        y_column,
        title=None
    ):

        clean_df = (
            df[[x_column, y_column]]
            .dropna()
            .sort_values(by=x_column)
        )

        plt.figure(figsize=(11, 6))

        ax = sns.lineplot(
            data=clean_df,
            x=x_column,
            y=y_column,
            marker="o"
        )

        plt.title(
            title or f"{y_column} por {x_column}",
            fontsize=16,
            fontweight='bold'
        )

        plt.xlabel(x_column)
        plt.ylabel(y_column)

        ax.yaxis.set_major_formatter(
            ChartService.thousands_formatter()
        )

        return ChartService.save_chart()


    # ==========================================
    # BOXPLOT
    # ==========================================

    @staticmethod
    def generate_boxplot(
        df,
        x_column,
        y_column,
        title=None
    ):

        clean_df = (
            df[[x_column, y_column]]
            .dropna()
        )

        plt.figure(figsize=(12, 6))

        ax = sns.boxplot(
            data=clean_df,
            x=x_column,
            y=y_column
        )

        plt.title(
            title or f"{y_column} por {x_column}",
            fontsize=16,
            fontweight='bold'
        )

        plt.xlabel(x_column)
        plt.ylabel(y_column)

        plt.xticks(
            rotation=45,
            ha="right"
        )

        ax.yaxis.set_major_formatter(
            ChartService.thousands_formatter()
        )

        return ChartService.save_chart()


    # ==========================================
    # VIOLINPLOT
    # ==========================================

    @staticmethod
    def generate_violinplot(
        df,
        x_column,
        y_column,
        title=None
    ):

        clean_df = (
            df[[x_column, y_column]]
            .dropna()
        )

        plt.figure(figsize=(12, 6))

        ax = sns.violinplot(
            data=clean_df,
            x=x_column,
            y=y_column
        )

        plt.title(
            title or f"{y_column} por {x_column}",
            fontsize=16,
            fontweight='bold'
        )

        plt.xlabel(x_column)
        plt.ylabel(y_column)

        plt.xticks(
            rotation=45,
            ha="right"
        )

        return ChartService.save_chart()


    # ==========================================
    # HEATMAP
    # ==========================================

    @staticmethod
    def generate_heatmap(
        df,
        title=None
    ):

        numeric_df = (
            df.select_dtypes(
                include=['number']
            )
        )

        if numeric_df.shape[1] < 2:

            return None

        correlation = numeric_df.corr()

        plt.figure(figsize=(10, 8))

        sns.heatmap(
            correlation,
            annot=True,
            fmt=".2f",
            cmap="coolwarm"
        )

        plt.title(
            title or "Mapa de correlación",
            fontsize=16,
            fontweight='bold'
        )

        return ChartService.save_chart()


    # ==========================================
    # MAIN AI CHART GENERATOR
    # ==========================================

    @staticmethod
    def generate_charts_from_ai(
        df,
        ai_analysis
    ):

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

                    chart = (
                        ChartService
                        .generate_histogram(
                            df,
                            item["x"],
                            item.get("title")
                        )
                    )

                    chart_paths.append(chart)

                # ==================================
                # COUNTPLOT
                # ==================================

                elif chart_type == "countplot":

                    chart = (
                        ChartService
                        .generate_countplot(
                            df,
                            item["x"],
                            item.get("title")
                        )
                    )

                    chart_paths.append(chart)

                # ==================================
                # BARPLOT
                # ==================================

                elif chart_type == "barplot":

                    chart = (
                        ChartService
                        .generate_barplot(
                            df,
                            item["x"],
                            item["y"],
                            item.get(
                                "aggregation",
                                "mean"
                            ),
                            item.get("title")
                        )
                    )

                    chart_paths.append(chart)

                # ==================================
                # SCATTERPLOT
                # ==================================

                elif chart_type == "scatterplot":

                    chart = (
                        ChartService
                        .generate_scatterplot(
                            df,
                            item["x"],
                            item["y"],
                            item.get("title")
                        )
                    )

                    chart_paths.append(chart)

                # ==================================
                # LINEPLOT
                # ==================================

                elif chart_type == "lineplot":

                    chart = (
                        ChartService
                        .generate_lineplot(
                            df,
                            item["x"],
                            item["y"],
                            item.get("title")
                        )
                    )

                    chart_paths.append(chart)

                # ==================================
                # BOXPLOT
                # ==================================

                elif chart_type == "boxplot":

                    chart = (
                        ChartService
                        .generate_boxplot(
                            df,
                            item["x"],
                            item["y"],
                            item.get("title")
                        )
                    )

                    chart_paths.append(chart)

                # ==================================
                # VIOLINPLOT
                # ==================================

                elif chart_type == "violinplot":

                    chart = (
                        ChartService
                        .generate_violinplot(
                            df,
                            item["x"],
                            item["y"],
                            item.get("title")
                        )
                    )

                    chart_paths.append(chart)

                # ==================================
                # HEATMAP
                # ==================================

                elif chart_type == "heatmap":

                    chart = (
                        ChartService
                        .generate_heatmap(
                            df,
                            item.get("title")
                        )
                    )

                    if chart:

                        chart_paths.append(chart)

                else:

                    print(
                        f"Unsupported chart type: "
                        f"{chart_type}"
                    )

            except Exception:

                import traceback

                print(
                    "\nERROR GENERATING CHART\n"
                )

                traceback.print_exc()

        return chart_paths