from django.urls import path
from . import views

urlpatterns=[
    path('satisfaction-data-form/', views.satisfaction_data_form, name='satisfaction_data_form'),
    path('satisfaction-data-display/', views.satisfaction_indicator_view, name='satisfaction_data_display'),
    
    path('manage-indicator/<int:indicator_id>/', views.manage_indicator, name='manage_indicator'),
    
    path('trust-in-local-authorities/', views.trust_in_local_authorities, name='trust_in_local_authorities'),
    
    path('indicator_list/', views.indicator_list, name='indicator_list'),
    
    path('indicators/indicator-detail/<int:indicator_id>/', views.indicator_detail, name='indicator_detail'),

    
    path('update-indicator-value/<int:id>/', views.update_indicator_value, name='update_indicator_value'),
]