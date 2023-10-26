from django.db import models
from django_mysql.models import ListCharField
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import magic
#from multiselectfield import MultiSelectField
#from django.contrib.auth.models import Group
#from django.contrib.auth.models import Permission
#from django.contrib.contenttypes.models import ContentType


LANGUAGE = (
        ('', 'Select a gender'),
        ('English', 'English'),
        ('Krio', 'Krio'),
        ('Mende', 'Mende'),
        ('Themne', 'Themne'),
        ('Kono', 'Kono'),
        ('Loko', 'Loko'),
        ('Sherbro', 'Sherbro'),
        ('Limba', 'Limba'),
        ('Fullah', 'Fullah'),
        ('Koranko', 'Koranko'),
        ('Yalunka', 'Yalunka'),
        ('Madingo', 'Madingo'),
        ('Susu', 'Susu'),
        ('Vai', 'Vai'),
        ('Kru', 'Kru'),
        ('Gola', 'Gola'),
        ('Kissi', 'Kissi'),
        ('Other', 'Other'),
)

EDUCATION = (
        ('', 'Select level of education'),
        ('No Schooling', 'No Schooling'),
        ('Informal Schooling', 'Informal Schooling'),
        ('Primary School', 'Primary School'),
        ('Completed Primary School', 'Completed Primary School'),
        ('Secondary School', 'Secondary School'),
        ('Completed Secondary School', 'Completed Secondary School'),
        ('Post-secondary qualifications', 'Post-secondary qualifications, other than university e.g. a diploma or degree from a polytechnic or college'),
        ('Attending University', 'Attending University'),
        ('Completed University', 'Completed University'),
        ('Post-graduate', 'Post-graduate'),
        ('Refused to answer', 'Refused to answer'),
)

SATISFACTORY_LEVEL = (
        ('', 'Select level of satisfaction'),
        ('Very Satisfied', 'Very Satisfied'),
        ('Somewhat Satisfied', 'Somewhat Satisfied'),
        ('Very Dissatisfied', 'Very Dissatisfied'),
        ('Somewhat Dissatisfied', 'Somewhat Dissatisfied'),
        ('Neither', 'Neither'),
)

ACCESS_HEALTH_FACILITIES = (
        ('', 'Select access to health facilities'),
        ('Very easy', 'Very easy'),
        ('Somewhat easy', 'Somewhat easy'),
        ('Somewhat difficult', 'Somewhat difficult'),
        ('Very difficult', 'Very difficult'),
        ("Don't know ", "Don't know "),
)

OCCUPATION = (
        ('', 'Select an occupation'),
        ('Never had a job', 'Never had a job'),
        ('Student', 'Student'),
        ('Housewife / Homemaker', 'Housewife / Homemaker'),
        ('Agriculture / Farming / Fishing / Forestry', 'Agriculture / Farming / Fishing / Forestry'),
        ('Trader / Hawker / Vendor', 'Trader / Hawker / Vendor'),
        ('Retail / Shop', 'Retail / Shop'),
        ('Unskilled manual worker', 'Unskilled manual worker (e.g. cleaner, laborer, domestic help, unskilled manufacturing worker)'),
        ('Artisan or skilled manual worker', 'Artisan or skilled manual worker (e.g. trades like electrician, mechanic, machinist, or skilled manufacturing worker)'),
        ('Clerical or secretarial', 'Clerical or secretarial'),
        ('Supervisor / Foreman / Senior manager', 'Supervisor / Foreman / Senior manager'),
        ('Security services', 'Security services (police, army, private security)'),
        ('Mid-level professional', 'Mid-level professional (e.g. teacher, nurse, mid-level government officer)'),
        ('Upper-level professional', 'Upper-level professional (e.g. banker / finance, doctor, lawyer, engineer, accountant, professor, senior-level government officer)'),
        ('Other', 'Other'),
)

GENDER = (
        ('', 'Select a language'),
        ('Male', 'Male'),
        ('Female', 'Female'),
)

class District(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Districts"
    
    def __str__(self):
        return self.name
    
class Chiefdom(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Chiefdoms"
    
    def __str__(self):
        return self.name

class School(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="School District")
    
    chiefdom = models.CharField(max_length=255)
    
    town_or_village_name = models.CharField(max_length=255)
    
    school_name = models.CharField(max_length=250)
    
    total_girl_students = models.PositiveIntegerField(default=0)
    
    total_boy_students = models.PositiveIntegerField(default=0)
    
    total_female_teachers = models.PositiveIntegerField(default=0)
    
    total_male_teachers = models.PositiveIntegerField(default=0)
    
    total_qualified_teachers = models.PositiveIntegerField(default=0)
    
    total_untrained_teachers = models.PositiveIntegerField(default=0)
    
    total_teachers_with_pin_code = models.PositiveIntegerField(default=0)
    
    total_teachers_without_pin_code = models.PositiveIntegerField(default=0)
    
    shifts_per_day = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Schools"
    
    def __str__(self):
        return self.school_name
    
    
class CitizenDemographics(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    chiefdom = models.ForeignKey(Chiefdom, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER)
    age = models.CharField(max_length=3)
    language = models.CharField(max_length=100, choices=LANGUAGE)
    education = models.CharField(max_length=150, choices=EDUCATION)
    occupation = models.CharField(max_length=250, choices=OCCUPATION)
    
    class Meta:
        verbose_name_plural = "Citizen Demographics"
        
class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Service Type"
    
    def __str__(self):
        return self.name

class SatisfactionSurvey(models.Model):
    citizen = models.ForeignKey(CitizenDemographics, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    level_of_satisfactory = models.CharField(max_length=255, blank=True, null=True, choices=SATISFACTORY_LEVEL, verbose_name="How satisfied are you with these services?")
    easy_or_difficulty_to_access_medical_facilities = models.TextField(max_length=100, blank=True, null=True, choices=ACCESS_HEALTH_FACILITIES, verbose_name="How easy or difficult is it to obtain the medical care you and your family need by government health facilities?")
    date_submitted = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.citizen} - {self.service_type} Satisfaction Survey"
    



class LocalCouncil(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Local Councils"
    
    def __str__(self):
        return self.name
    



