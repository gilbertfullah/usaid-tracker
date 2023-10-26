from django.contrib import admin
from .models import LocalCouncil, DistrictCSO, MDA, MLGRD, Assignment, Role, Ministry, Notification
from django.utils.html import format_html

class DistrictCSOAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 10
    
class LocalCouncilAdmin(admin.ModelAdmin):
    list_display = ['username']
    list_per_page = 10
    
class MDAAdmin(admin.ModelAdmin):
    list_display = ['username']
    list_per_page = 10
    
class MLGRDAdmin(admin.ModelAdmin):
    list_display = ['username']
    list_per_page = 10
    
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 10
    
class MinistryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 10
    
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['message']
    list_per_page = 10
    
    
admin.site.register(DistrictCSO, DistrictCSOAdmin)
admin.site.register(LocalCouncil, LocalCouncilAdmin)
admin.site.register(MDA, MDAAdmin)
admin.site.register(MLGRD, MLGRDAdmin)
admin.site.register(Assignment)
admin.site.register(Role, RoleAdmin)
admin.site.register(Ministry, MinistryAdmin)
admin.site.register(Notification, NotificationAdmin)
