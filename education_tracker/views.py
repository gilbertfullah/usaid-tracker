from django.shortcuts import render
from schools.models import School, District, ServiceType
from django.db.models import Avg
from django.db.models import Count, F, ExpressionWrapper, FloatField
from decimal import Decimal
from indicators.models import IndicatorData, CitizenPrioritiesData, CitizenPrioritiesData, TrustInLocalAuthorities, NPSEResults, CommunityStability, \
    BudgetAllocation, BriberyReductionData
from datetime import datetime

def index(request):
    
    # Define the target answer_choice and date_submitted values
    trust_indicator = f"% increase in citizen’s trust in local authorities"
    target_choice = 'A lot'
    target_date_2018 = datetime(2018, 10, 25)
    target_date_2020 = datetime(2020, 10, 25)
    target_date_2022 = datetime(2022, 10, 25)

    # Calculate the average indicator_value for each target
    avg_2018 = Decimal(IndicatorData.objects.filter(answer_choice_trust=target_choice, date_submitted=target_date_2018, status='approved', indicator__name=trust_indicator).
                    aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_2018 = round(avg_2018, 2)
    
    avg_2020 = Decimal(IndicatorData.objects.filter(answer_choice_trust=target_choice, date_submitted=target_date_2020, status='approved', indicator__name=trust_indicator).
                    aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_2020 = round(avg_2020, 2)

    avg_2022 = Decimal(IndicatorData.objects.filter(answer_choice_trust=target_choice, date_submitted=target_date_2022, status='approved', indicator__name=trust_indicator).
                    aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_2022 = round(avg_2022, 2) 

    # Define color and arrow direction based on the average values
    def get_color_and_arrow(avg_value):
        if avg_value <= 34:
            return 'red', 'down'
        elif 35 <= avg_value <= 49:
            return 'orange', 'right'
        else:
            return 'green', 'up'

    color_2018, arrow_2018 = get_color_and_arrow(avg_2018)
    color_2020, arrow_2020 = get_color_and_arrow(avg_2020)
    color_2022, arrow_2022 = get_color_and_arrow(avg_2022)
    
    # Calculate the average indicator_value for all districts where status is approved
    npse_indicator = f"% increase learning outcomes as reflected in the NPSE scores in focused districts"
    
    avg_npse_values = Decimal(IndicatorData.objects.filter(status='approved', indicator__name=npse_indicator).
                    aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_npse_values = round(avg_npse_values, 0)
    
    # Define color and arrow direction based on the average values
    def get_color_and_arrow(avg_npse_values):
        if avg_npse_values <= 230:
            return 'red', 'down'
        elif 231 <= avg_npse_values <= 240:
            return 'orange', 'right'
        else:
            return 'green', 'up'
    
    # Define color and arrow direction based on the average values
    npse_color, npse_arrow = get_color_and_arrow(avg_npse_values)
    
    # Define the target answer_choice and date_submitted values
    target_answer_choice = 'Very much'

    # Calculate the average indicator_value for each target
    avg_com_stability = Decimal(IndicatorData.objects.filter(answer_choice_comm_stability=target_answer_choice, status='approved').
                                aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_com_stability = round(avg_com_stability, 2)


    # Define color and arrow direction based on the average values
    def get_color_and_arrow(avg_com_stability):
        if avg_com_stability <= 34:
            return 'red', 'down'
        elif 35 <= avg_com_stability <= 49:
            return 'orange', 'right'
        else:
            return 'green', 'up'

    stability_color, stability_arrow = get_color_and_arrow(avg_com_stability)
    
    # Define the target answer_choice and date_submitted values
    budget_indicator = f"% of budget allocated to devolved functions"
    
    budget_date_2020 = datetime(2020, 10, 25)
    budget_date_2021 = datetime(2021, 10, 25)
    budget_date_2022 = datetime(2022, 10, 25)

    # Calculate the average indicator_value for each target
    avg_budget_2020 = Decimal(IndicatorData.objects.filter(date_submitted=budget_date_2020, status='approved', indicator__name=budget_indicator).aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_budget_2020 = round(avg_budget_2020, 2)
    
    avg_budget_2021 = Decimal(IndicatorData.objects.filter(date_submitted=budget_date_2021, status='approved', indicator__name=budget_indicator).aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_budget_2021 = round(avg_budget_2021, 2)

    avg_budget_2022 = Decimal(IndicatorData.objects.filter(date_submitted=budget_date_2022, status='approved', indicator__name=budget_indicator).aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_budget_2022 = round(avg_budget_2022, 2) 

    # Define color and arrow direction based on the average values
    def get_color_and_arrow(budget_avg_value):
        if budget_avg_value <= 34:
            return 'red', 'down'
        elif 35 <= budget_avg_value <= 49:
            return 'orange', 'right'
        else:
            return 'green', 'up'

    budget_color_2020, budget_arrow_2020 = get_color_and_arrow(avg_budget_2020)
    budget_color_2021, budget_arrow_2021 = get_color_and_arrow(avg_budget_2021)
    budget_color_2022, budget_arrow_2022 = get_color_and_arrow(avg_budget_2022)
    
    # Define the target answer_choice and date_submitted values
    media_outlet = 'Radio'

    # Calculate the average indicator_value for each target
    bribery_service = "Medical services"
    avg_bribery_service = Decimal(IndicatorData.objects.filter(bribery_services=bribery_service, status='approved').
                                aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_bribery_service  = round(avg_bribery_service, 2)


    # Define color and arrow direction based on the average values
    def get_color_and_arrow(avg_bribery_service):
        if avg_bribery_service <= 34:
            return 'red', 'down'
        elif 35 <= avg_bribery_service <= 49:
            return 'orange', 'right'
        else:
            return 'green', 'up'

    bribery_service_color, bribery_service_arrow = get_color_and_arrow(avg_bribery_service)
    
    # Define the target answer_choice and date_submitted values
    media_outlet = 'Radio'

    # Calculate the average indicator_value for each target
    avg_media_outlet = Decimal(IndicatorData.objects.filter(media_outlets=media_outlet, status='approved').
                                aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_media_outlet  = round(avg_media_outlet, 2)


    # Define color and arrow direction based on the average values
    def get_color_and_arrow(avg_media_outlet):
        if avg_media_outlet <= 34:
            return 'red', 'down'
        elif 35 <= avg_media_outlet <= 49:
            return 'orange', 'right'
        else:
            return 'green', 'up'

    media_outlet_color, media_outlet_arrow = get_color_and_arrow(avg_media_outlet)
    
    # Calculate the average indicator_value for all districts where status is approved
    audit_recommendation_indicator = f"% increase in audit recommendations implemented by the councils"
    
    avg_audit_recommendation = Decimal(IndicatorData.objects.filter(status='approved', indicator__name=audit_recommendation_indicator).
                    aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_audit_recommendation = round(avg_audit_recommendation, 0)
    
    # Define color and arrow direction based on the average values
    def get_color_and_arrow(avg_audit_recommendation):
        if avg_audit_recommendation <= 230:
            return 'red', 'down'
        elif 231 <= avg_audit_recommendation <= 240:
            return 'orange', 'right'
        else:
            return 'green', 'up'
    
    # Define color and arrow direction based on the average values
    audit_recommendation_color, audit_recommendation_arrow = get_color_and_arrow(avg_audit_recommendation)
    
    # Calculate the average indicator_value for all districts where status is approved
    audit_lc_misuse = f"% Reduction in citizens who believe local councils misuse revenue"
    
    avg_lc_misuse = Decimal(IndicatorData.objects.filter(status='approved', indicator__name=audit_lc_misuse).
                    aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_lc_misuse = round(avg_lc_misuse, 0)
    
    # Define color and arrow direction based on the average values
    def get_color_and_arrow(avg_lc_misuse):
        if avg_lc_misuse <= 230:
            return 'red', 'down'
        elif 231 <= avg_lc_misuse <= 240:
            return 'orange', 'right'
        else:
            return 'green', 'up'
    
    # Define color and arrow direction based on the average values
    lc_misuse_color, lc_misuse_arrow = get_color_and_arrow(avg_lc_misuse)
    
    
    # Calculate the average indicator_value for all districts where status is approved
    lc_budget_indicator = f"% of citizens who are aware of local council budget"
    
    avg_lc_budget = Decimal(IndicatorData.objects.filter(status='approved', indicator__name=lc_budget_indicator).
                    aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_lc_budget = round(avg_lc_budget, 0)
    
    # Define color and arrow direction based on the average values
    def get_color_and_arrow(avg_lc_budget):
        if avg_lc_budget <= 230:
            return 'red', 'down'
        elif 231 <= avg_lc_budget <= 240:
            return 'orange', 'right'
        else:
            return 'green', 'up'
    
    # Define color and arrow direction based on the average values
    lc_budget_color, lc_budget_arrow = get_color_and_arrow(avg_lc_budget)
    
    
    # Calculate the average indicator_value for all districts where status is approved
    lc_project_indicator = f"% of citizens who are aware of local council projects"
    
    avg_lc_project = Decimal(IndicatorData.objects.filter(status='approved', indicator__name=lc_project_indicator).
                    aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_lc_project = round(avg_lc_project, 0)
    
    # Define color and arrow direction based on the average values
    def get_color_and_arrow(avg_lc_project):
        if avg_lc_project <= 230:
            return 'red', 'down'
        elif 231 <= avg_lc_project <= 240:
            return 'orange', 'right'
        else:
            return 'green', 'up'
    
    # Define color and arrow direction based on the average values
    lc_project_color, lc_project_arrow = get_color_and_arrow(avg_lc_project)
    
    
    # Define color and arrow direction based on the average values
    lc_budget_color, lc_budget_arrow = get_color_and_arrow(avg_lc_budget)
    
    
    # Calculate the average indicator_value for all districts where status is approved
    joint_advocacy_indicator = f"Number of joint advocacy initiatives implemented by LCs and CSOs"
    
    avg_joint_advocacy = Decimal(IndicatorData.objects.filter(status='approved', indicator__name=joint_advocacy_indicator).
                    aggregate(Avg('indicator_value'))['indicator_value__avg'] or 0)
    avg_joint_advocacy = round(avg_joint_advocacy, 0)
    
    # Define color and arrow direction based on the average values
    def get_color_and_arrow(avg_joint_advocacy):
        if avg_joint_advocacy <= 230:
            return 'red', 'down'
        elif 231 <= avg_joint_advocacy <= 240:
            return 'orange', 'right'
        else:
            return 'green', 'up'
    
    # Define color and arrow direction based on the average values
    joint_advocacy_color, joint_advocacy_arrow = get_color_and_arrow(avg_joint_advocacy)

    
    context = {
        'avg_2018': avg_2018,
        'avg_2020': avg_2020,
        'avg_2022': avg_2022,
        'color_2018': color_2018,
        'color_2020': color_2020,
        'color_2022': color_2022,
        'arrow_2018': arrow_2018,
        'arrow_2020': arrow_2020,
        'arrow_2022': arrow_2022,
        
        'avg_npse_values':avg_npse_values,
        'npse_color':npse_color,
        'npse_arrow':npse_arrow,
        
        'avg_com_stability':avg_com_stability,
        'stability_color':stability_color,
        'stability_arrow':stability_arrow,
        
        'avg_budget_2020': avg_budget_2020,
        'avg_budget_2021': avg_budget_2021,
        'avg_budget_2022': avg_budget_2022,
        'budget_color_2020': budget_color_2020,
        'budget_color_2021': budget_color_2021,
        'budget_color_2022': budget_color_2022,
        'budget_arrow_2020': budget_arrow_2020,
        'budget_arrow_2021': budget_arrow_2021,
        'budget_arrow_2022': budget_arrow_2022,
        
        'avg_bribery_service': avg_bribery_service,
        'bribery_service_color': bribery_service_color,
        'bribery_service_arrow': bribery_service_arrow,
        
        'avg_media_outlet':avg_media_outlet,
        'media_outlet_color':media_outlet_color,
        'media_outlet_arrow':media_outlet_arrow,
        
        'avg_audit_recommendation':avg_audit_recommendation,
        'audit_recommendation_color':audit_recommendation_color,
        'audit_recommendation_arrow':audit_recommendation_arrow,
        
        'avg_lc_misuse':avg_lc_misuse,
        'lc_misuse_color':lc_misuse_color,
        'lc_misuse_arrow':lc_misuse_arrow,
        
        'avg_lc_budget':avg_lc_budget,
        'lc_budget_color':lc_budget_color,
        'lc_budget_arrow':lc_budget_arrow,
        
        'avg_lc_project':avg_lc_project,
        'lc_project_color':lc_project_color,
        'lc_project_arrow':lc_project_arrow,
        
        'avg_joint_advocacy':avg_joint_advocacy,
        'joint_advocacy_color':joint_advocacy_color,
        'joint_advocacy_arrow':joint_advocacy_arrow,
        
    }
    
    return render(request, 'index.html', context)
