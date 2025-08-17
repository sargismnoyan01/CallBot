from django.urls import path
from . import views

urlpatterns = [
    path('call/', views.make_call, name='make_call'),
]
