from django import forms
from .models import IndicatorData, CitizenPrioritiesData
from django.db import transaction

    
    
class IndicatorDataForm(forms.ModelForm):
    class Meta:
        model = IndicatorData
        fields = ['indicator_value']  # Include all fields from the IndicatorData model
        # You can also exclude fields if necessary: exclude = ['field_to_exclude']
        
class CitizenPrioritiesForm(forms.ModelForm):
    class Meta:
        model = CitizenPrioritiesData
        fields = '__all__'
        