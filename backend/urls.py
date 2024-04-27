"""
URL configuration for cpd_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from backend.views import change_cpd_plan_status, create_cpd_item, create_cpd_plan, create_new_user, delete_cpd_plan, download_cpd_summary, edit_profile, get_format_of_training, get_home_data, get_home_data_web, get_skills_area, list_my_cpd_items, list_my_cpd_plans, logout, sign_in
urlpatterns = [
        path('create_new_user',create_new_user,name="create_new_user"),
        path('sign_in',sign_in,name="sign_in"),
        path('logout',logout,name="logout"),
        path('edit_profile',edit_profile,name="edit_profile"),
        path('get_skills_area',get_skills_area,name="get_skills_area"),
        path('get_format_of_training',get_format_of_training,name="get_format_of_training"),
        path('create_cpd_item',create_cpd_item,name="create_cpd_item"),
        path('list_my_cpd_items',list_my_cpd_items,name="list_my_cpd_items"),
        path('get_home_data',get_home_data,name="get_home_data"),
        path('get_home_data_web',get_home_data_web,name="get_home_data_web"),
        path('create_cpd_plan',create_cpd_plan,name="create_cpd_plan"),
        path('change_cpd_plan_status',change_cpd_plan_status,name="change_cpd_plan_status"),
        path('list_my_cpd_plans',list_my_cpd_plans,name="list_my_cpd_plans"),
        path('delete_cpd_plan',delete_cpd_plan,name="delete_cpd_plan"),
        path('download_cpd_summary',download_cpd_summary,name="download_cpd_summary"),
        
        
]
