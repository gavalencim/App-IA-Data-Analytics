from django.urls import path
from .views import (home, dataset_chat)

urlpatterns = [
    path('', home, name='home'),
    path("dataset-chat/", dataset_chat, name="dataset_chat"),
]