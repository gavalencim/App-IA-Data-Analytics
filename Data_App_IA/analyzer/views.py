import json
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from .services.csv.csv_service import CSVService
from .services.visualization.chart_service import (
    ChartService
)
from .services.ai.dataset_ai_service import (
    DatasetAIService
)
from .services.ai.dataset_ai_rag_service import (
    DatasetRAGService
)
CURRENT_DATAFRAME = None


def home(request):

    global CURRENT_DATAFRAME

    context = {}

    # ====================================
    # PASO 1
    # SUBIR CSV
    # ====================================

    if request.method == "POST" and request.FILES.get("csv_file"):

        csv_file = request.FILES.get("csv_file")

        df = CSVService.load_csv(csv_file)

        CURRENT_DATAFRAME = df

        # Guardar temporalmente dataset
        df.to_csv("temp_dataset.csv", index=False)

        dataset_info = (
            CSVService.get_basic_info(df)
        )

        preview = (
            CSVService.get_preview(df)
        )

        column_types = (
            CSVService.detect_column_types(df)
        )

        context = {
            "dataset_info": dataset_info,
            "preview": preview,
            "column_types": column_types,
            "show_analysis_form": True
        }

    # ====================================
    # PASO 2
    # ANALISIS IA
    # ====================================

    elif request.method == "POST" and request.POST.getlist("selected_columns"):

        selected_columns = (
            request.POST.getlist(
                "selected_columns"
            )
        )

        analysis_goal = (
            request.POST.get(
                "analysis_goal"
            )
        )

        df = pd.read_csv("temp_dataset.csv")

        CURRENT_DATAFRAME = df

        # Limitar columnas

        filtered_df = df[selected_columns]

        dataset_profile = (
            DatasetAIService
            .build_dataset_profile(
                filtered_df
            )
        )

        ai_analysis = (
            DatasetAIService
            .analyze_dataset(
                dataset_profile,
                analysis_goal, selected_columns
            )
        )

        charts = (
            ChartService
            .generate_charts_from_ai(
                filtered_df,
                ai_analysis
            )
        )

        context = {
            "charts": charts,
            "ai_analysis": ai_analysis,
            "analysis_goal": analysis_goal
        }

    return render(
        request,
        "analyzer/home.html",
        context
    )

def dataset_chat(request):

    global CURRENT_DATAFRAME

    if request.method == "POST":

        question = request.POST.get(
            "question")

        if CURRENT_DATAFRAME is None:

            return JsonResponse({
                "answer":
                    "No dataset loaded."
            })

        response = (
            DatasetRAGService
            .ask_dataset(
                question,
                CURRENT_DATAFRAME
            )
        )
        return JsonResponse(response)

    return JsonResponse({
        "answer":
            "Invalid request."
    })