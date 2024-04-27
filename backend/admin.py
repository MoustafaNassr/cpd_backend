from django.contrib import admin
from .models import Profile, SkillArea, FormatOfTraining, CPDItem, CPDPlan

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profession_title')
    search_fields = ('user__username', 'profession_title')

@admin.register(SkillArea)
class SkillAreaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(FormatOfTraining)
class FormatOfTrainingAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(CPDItem)
class CPDItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'type', 'skills_area', 'format_of_training', 'hours_logged', 'date_completed', 'cost_of_cpd')
    list_filter = ('type', 'skills_area', 'format_of_training')
    search_fields = ('title', 'user__username')
    date_hierarchy = 'date_completed'



@admin.register(CPDPlan)
class CPDPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'status','user')
    list_filter = ('status',)
    search_fields = ('title', 'user')
