from django.shortcuts import render, redirect, get_object_or_404
from .forms import SatisfactionSurveyForm
from .models import SatisfactionSurvey, ServiceType, CitizenDemographics, District
from django.core.paginator import Paginator
import os
from django.conf import settings
import calendar
from django.db.models.functions import ExtractMonth, ExtractHour, ExtractDay
from django.db.models import Count, CharField, Value
from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import TruncDate, Cast
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from functools import wraps
from django.db.models import Avg
from django.db.models import Count, F, ExpressionWrapper, FloatField
from indicators.models import ServiceType, IndicatorData
from django.http import JsonResponse
import json
from indicators.models import CitizenPrioritiesData





def satisfaction_survey_form(request):
    if request.method == 'POST':
        form = SatisfactionSurveyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to a success page
    else:
        form = SatisfactionSurveyForm()

    return render(request, 'satisfaction_survey_form.html', {'form': form})

def satisfaction_survey_chart(request):
    # Get all available districts and service types
    all_districts = District.objects.all()
    all_service_types = ServiceType.objects.all()

    # Get filtering parameters from the request
    selected_district = request.GET.get('district', '')
    selected_service_type = request.GET.get('service_type', '')

    # Filter the survey data based on selected parameters
    survey_data = SatisfactionSurvey.objects.all()
    if selected_district:
        survey_data = survey_data.filter(citizen__district=selected_district)
    if selected_service_type:
        survey_data = survey_data.filter(service_type=selected_service_type)

    # Calculate aggregated data for the chart, including percentage
    total_responses = survey_data.count()
    
    # Calculate the percentage of "very satisfied" responses
    very_satisfied_percentage = survey_data.filter(level_of_satisfactory='Very Satisfied').count() * 100.0 / total_responses

    # Calculate the percentage of "somewhat satisfied" responses
    somewhat_satisfied_percentage = survey_data.filter(level_of_satisfactory='Somewhat Satisfied').count() * 100.0 / total_responses

    # Calculate the combined percentage
    satisfied_combined_percentage = very_satisfied_percentage + somewhat_satisfied_percentage
    
    # Calculate the percentage of "very dissatisfied" responses
    very_dissatisfied_percentage = survey_data.filter(level_of_satisfactory='Very Dissatisfied').count() * 100.0 / total_responses

    # Calculate the percentage of "somewhat dissatisfied" responses
    somewhat_dissatisfied_percentage = survey_data.filter(level_of_satisfactory='Somewhat Dissatisfied').count() * 100.0 / total_responses

    # Calculate the combined percentage
    dissatisfied_combined_percentage = very_dissatisfied_percentage + somewhat_dissatisfied_percentage

    

    context = {
        'all_districts': all_districts,
        'all_service_types': all_service_types,
        'selected_district': selected_district,
        'selected_service_type': selected_service_type,
        'satisfied_combined_percentage': satisfied_combined_percentage,
        'dissatisfied_combined_percentage': dissatisfied_combined_percentage,
        'labels': ["Satisfied", "Dissatisfied"],
        'data': [satisfied_combined_percentage, dissatisfied_combined_percentage],
    }

    return render(request, 'satisfaction_survey.html', context)


def indicator_progress_view(request):
    # Get all service types
    service_types = ServiceType.objects.all()

    # Initialize an empty dictionary to store data for each service type
    data_by_service_type = {}

    # Loop through service types to fetch data and calculate averages
    for service_type in service_types:
        # Filter IndicatorData entries for the current service type
        indicator_data = IndicatorData.objects.filter(service_type=service_type)

        # Calculate the average percentage of indicator_value for each date_submitted
        avg_data = indicator_data.values('date_submitted').annotate(avg_percentage=Avg('indicator_value'))

        # Extract date and average percentage data
        dates = [entry['date_submitted'] for entry in avg_data]
        percentages = [entry['avg_percentage'] for entry in avg_data]

        # Store the data for the current service type
        data_by_service_type[service_type.name] = {
            'dates': dates,
            'percentages': percentages,
        }

    # Collect dates and values for each service type
    dates_by_service_type = {}
    values_by_service_type = {}

    for service_type, data in data_by_service_type.items():
        dates_by_service_type[service_type] = data['dates']
        values_by_service_type[service_type] = data['percentages']

    context = {
        'service_types': service_types,
        'data_by_service_type': data_by_service_type,
        'dates_by_service_type': dates_by_service_type,
        'values_by_service_type': values_by_service_type,
    }

    return render(request, 'satisfaction_survey.html', context)


def calculate_average_data(district_id=None):
    service_types = ServiceType.objects.all()
    data = []

    for service_type in service_types:
        indicator_values = IndicatorData.objects.filter(service_type=service_type)
        if district_id:
            indicator_values = indicator_values.filter(district_id=district_id)
        avg_value = indicator_values.aggregate(avg_value=Avg('indicator_value'))['avg_value']
        data.append({
            'service_type': service_type.name,
            'avg_value': avg_value,
        })

    return data

def chart_view(request):
    # Get a list of unique service types
    service_types = IndicatorData.objects.values_list('service_type__name', flat=True).distinct()
    
    # Get the distinct dates
    dates = IndicatorData.objects.values_list('date_submitted', flat=True).distinct().order_by('date_submitted')
    
    # Create a dictionary to store data for each service type
    data_by_service_type = {service_type: [] for service_type in service_types}
    
    # Optionally, retrieve a list of all districts for the filter dropdown
    districts = District.objects.all()
    
    # By default, get the data for all districts
    selected_district = None
    
    if request.GET.get('district'):
        selected_district = District.objects.get(id=request.GET['district'])
    
    for date in dates:
        for service_type in service_types:
            # Calculate the average indicator value for the specified date, service type, and district (if selected)
            queryset = IndicatorData.objects.filter(date_submitted=date, service_type__name=service_type)
            if selected_district:
                queryset = queryset.filter(district=selected_district)
            avg_value = queryset.aggregate(Avg('indicator_value'))['indicator_value__avg']
            data_by_service_type[service_type].append(avg_value)
    
    context = {
        'service_types': service_types,
        'dates': dates,
        'data_by_service_type': data_by_service_type,
        'selected_district': selected_district,
        'districts': districts,
    }
    
    return render(request, 'satisfaction_survey.html', context)

def chart_data_view(request):
    district_id = request.GET.get('district_id')
    data = calculate_average_data(district_id)
    return JsonResponse(data, safe=False)


def citizen_priorities_view(request):
    # Get the selected district from the URL parameter or use None if not provided
    district_id = request.GET.get('district')
    
    # Get all available districts for the filter dropdown
    districts = District.objects.all()
    
    # Build the base queryset
    base_query = CitizenPrioritiesData.objects.annotate(month=ExtractMonth("date_submitted")).values("month")
    
    if district_id:
        # Filter the query by the selected district if provided
        base_query = base_query.filter(district=district_id)
    
    # Annotate and filter the query to calculate the average indicator values
    indicator_values = base_query.annotate(avg_value=Avg("indicator_value")).values('month', 'avg_value')

    month = []
    avg_indicator_values = []

    for values in indicator_values:
        month.append(calendar.month_name[values['month']])
        
        # Extract the numeric value from the Decimal object and round it to 2 decimal places
        avg_value = float(values['avg_value'])
        avg_indicator_values.append(round(avg_value, 2))

    context = {
        'districts': districts,
        'selected_district': district_id,
        'month': month,
        'avg_indicator_values': avg_indicator_values,
    }
    
    return render(request, 'citizen_priorities_view.html', context)