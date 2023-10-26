from django import forms
from .models import School, SatisfactionSurvey, ServiceType
from django.db import transaction
from django.core.validators import RegexValidator, FileExtensionValidator
        
class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'
        
class SatisfactionSurveyForm(forms.ModelForm):
    class Meta:
        model = SatisfactionSurvey
        fields = '__all__'
        