from django.urls import path
from .views import *


urlpatterns = [
    path("", mic, name="mic"),
]