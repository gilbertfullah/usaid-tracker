from django.urls import path
from . import views

urlpatterns=[
    
    path('satisfaction_survey/', views.chart_view, name='satisfaction_survey'),
    
    path('citizen_priorities_view/', views.citizen_priorities_view, name='citizen_priorities_view'),
    
    path('satisfaction-survey/', views.satisfaction_survey_form, name='satisfaction_survey_form'),
]