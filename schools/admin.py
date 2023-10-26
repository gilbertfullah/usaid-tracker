from django.contrib import admin
from .models import District, CitizenDemographics, ServiceType, SatisfactionSurvey
from django.utils.html import format_html


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 10
    
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 10


    
    
admin.site.register(District, DistrictAdmin)
admin.site.register(CitizenDemographics)
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(SatisfactionSurvey)