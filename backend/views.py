import os
from django.shortcuts import render
from cpd_django.settings import BASE_DIR
from rest_framework import serializers
from .models import Profile, SkillArea, FormatOfTraining, CPDItem, CPDPlan
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from weasyprint import HTML
from django.template.loader import render_to_string
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'profile_image', 'profession_title', 'user']

class SkillAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillArea
        fields = ['id', 'name']

class FormatOfTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormatOfTraining
        fields = ['id', 'name']

class CPDItemSerializer(serializers.ModelSerializer):
    skills_area = SkillAreaSerializer()
    format_of_training  =FormatOfTrainingSerializer()
    class Meta:
        model = CPDItem
        fields = ['id', 'user', 'title', 'type', 'skills_area', 'format_of_training', 
                  'hours_logged', 'date_completed', 'cost_of_cpd', 'what_did_you_learn', 
                  'future_dev_notes']
        
class CPDPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPDPlan
        fields = "__all__"

@api_view(
    [
        "POST",
    ]
)
def create_new_user(request):
    if request.method == "POST":
        email = request.data.get('email')
        password = request.data.get('password')
        profession_title = request.data.get('profession_title')
        profile_image = request.data.get('profile_image')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        if User.objects.filter(username=email).exists():
            data = {
                "success":False,
                "message":"This email already exists within our databases "
            }
            return Response(data, status=401)
        else:
            try:
                new_user = User.objects.create_user(username=email,password=password,first_name=first_name,last_name=last_name)
                new_token = Token.objects.create(user=new_user)
                new_profile = Profile.objects.create(user=new_user,profession_title=profession_title,profile_image=profile_image)
                user_data = {
                    "token":new_token.key,
                    "user":{
                    "id":new_user.id,
                    "email":new_user.username,
                    "first_name":new_user.first_name,
                    "last_name":new_user.last_name,
                    "profession_title" : new_profile.profession_title
                    }
                }
                if new_profile.profile_image:
                    user_data['user']['profile_image'] = new_profile.profile_image.url
                data = user_data
                return Response(data, status=200)
            except():
                data = {
                "success": False,
                "message":"Something went wrong"
                }
                return Response(data, status=500)

@api_view(
    [
        "POST",
    ]
)
def sign_in(request):
    data = {}
    if request.method == "POST":
        username = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            data['success'] = False
            data['message'] = "wrong username or password"
            return Response(data, status=401)
        else:
            if Token.objects.filter(user=user).exists():
                old_token = Token.objects.filter(user=user)
                old_token.delete()
            new_token = Token.objects.create(user=user)
            user_profile = user.profile.all()[0]

            user_data = {
                    "token":new_token.key,
                    "user":{
                    "id":user.id,
                    "email":user.username,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "profession_title" : user_profile.profession_title
                    }
                }
            if user_profile.profile_image:
                    user_data['user']['profile_image'] = user_profile.profile_image.url
            data = user_data
            return Response(data, status=200)

@api_view(
    [
        "GET",
    ]
)
def logout(request):
    data = {}
    if request.method == "GET":
        # Retrieve the token from the request headers
        token_key = request.headers.get("Authorization").split(" ")[1]
        
        # Query the Token model to find the corresponding user
        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            data["success"] = False
            data["message"] = "Invalid token"
            return Response(data, status=401)

        # Delete the token
        token.delete()

        data["success"] = True
        data["message"] = "Logout successful"
        return Response(data, status=200)
    
@api_view(
    [
        "POST",
    ]
)
def edit_profile(request):
    data = {}
    if request.method == "POST":
        # Query the Token model to find the corresponding user
        try:
            # Retrieve the token from the request headers
            token_key = request.headers.get("Authorization").split(" ")[1]
            token = Token.objects.get(key=token_key)
            user = token.user
            username = request.data.get('email')
            profession_title = request.data.get('profession_title')
            profile_image = request.data.get('profile_image')
            profile_objet = user.profile.all()[0]
            if username:
                user.username = username
                user.save()
            if profession_title:
                profile_objet.profession_title = profession_title
                profile_objet.save()
            if profile_image:
                profile_objet.profile_image=profile_image
                profile_objet.save()
            profile_ser = ProfileSerializer(profile_objet)
            data["success"] = True
            data["data"] = {"email":user.username,"token" : token_key}
            data['profile'] = profile_ser.data
            return Response(data, status=200)
        except Token.DoesNotExist:
            data["success"] = False
            data["message"] = "Invalid token"
            return Response(data, status=401)
        
@api_view(
    [
        "GET",
    ]
)
def get_skills_area(request):
    data = {}
    if request.method == "GET":
        all_skills = SkillArea.objects.all()
        skill_serializer = SkillAreaSerializer(all_skills,many=True)
        data["success"] = True
        data["data"] = skill_serializer.data
        return Response(data, status=200)

@api_view(
    [
        "GET",
    ]
)
def get_format_of_training(request):
    data = {}
    if request.method == "GET":
        all_formats = FormatOfTraining.objects.all()
        format_serializer = FormatOfTrainingSerializer(all_formats,many=True)
        data["success"] = True
        data["data"] = format_serializer.data
        return Response(data, status=200)
@api_view(
    [
        "POST",
    ]
)
def create_cpd_item(request):
    data = {}
    if request.method == "POST":
        # Query the Token model to find the corresponding user
        try:
            # Retrieve the token from the request headers
            token_key = request.headers.get("Authorization").split(" ")[1]
            # Get the user associated with the token and
            token_object = Token.objects.get(key=token_key)
            user_object = token_object.user
            title = request.data.get('title')
            type = request.data.get('type')
            skills_area = request.data.get('skills_area')
            skills_area_object = SkillArea.objects.get(id=skills_area)
            format_of_training = request.data.get('format_of_training')
            format_of_training_object = FormatOfTraining.objects.get(id=format_of_training)
            hours_logged = request.data.get('hours_logged')
            date_completed = request.data.get('date_completed')
            cost_of_cpd = request.data.get('cost_of_cpd')
            what_did_you_learn = request.data.get('what_did_you_learn')
            future_dev_notes = request.data.get('future_dev_notes')
            # file = request.data.get('file')
            new_cpd_item = CPDItem.objects.create(
                user=user_object,
                title=title,
                type=type,
                skills_area=skills_area_object,
                format_of_training=format_of_training_object,
                hours_logged=hours_logged,
                date_completed=date_completed,
                cost_of_cpd=cost_of_cpd,
                what_did_you_learn=what_did_you_learn,
                future_dev_notes=future_dev_notes,
                # file=file
            )
            data['success'] = True
            data['data'] = CPDItemSerializer(new_cpd_item).data
            return Response(data,status=201)
        except Token.DoesNotExist:
            data["success"] = False
            data["message"] = "Invalid token"
            return Response(data, status=401)

@api_view(
    [
        "GET",
    ]
)
def list_my_cpd_items(request):
    data = {}
    if request.method == "GET":
        try:
            token_key = request.headers.get("Authorization").split(" ")[1]
            token_object = Token.objects.get(key=token_key)
            user_object = token_object.user
            my_cpd_items = CPDItem.objects.filter(user=user_object)
            cpd_item_ser = CPDItemSerializer(my_cpd_items,many=True)
            data['success'] = True
            data['data'] = cpd_item_ser.data
            return Response(data,status=200)
        except Token.DoesNotExist:
            data["success"] = False
            data["message"] = "Invalid token"
            return Response(data, status=401)


@api_view(
    [
        "GET",
    ]
)
def get_home_data(request):
    data = {}
    if request.method == "GET":
        try:
            token_key = request.headers.get("Authorization").split(" ")[1]
            token_object = Token.objects.get(key=token_key)
            user_object = token_object.user
            my_cpd_items = CPDItem.objects.filter(user=user_object)
            hours_logged_list = list(my_cpd_items.values_list('hours_logged', flat=True))
            hours_logged_sum = sum(hours_logged_list)
            cpd_items_ser = CPDItemSerializer(my_cpd_items,many=True)
            data['success'] = True
            data['data'] = {
                "hours_logged":cpd_items_ser.data,
                "total_logged_hours":hours_logged_sum

            }
            return Response(data,status=200)
        except Token.DoesNotExist:
            data["success"] = False
            data["message"] = "Invalid token"
            return Response(data, status=401)


@api_view(
    [
        "GET",
    ]
)
def get_home_data_web(request):
    data = {}
    if request.method == "GET":
        try:
            token_key = request.headers.get("Authorization").split(" ")[1]
            token_object = Token.objects.get(key=token_key)
            user_object = token_object.user
            my_cpd_items = CPDItem.objects.filter(user=user_object)
            hours_logged_values_list = []
            hours_logged_titles_list = []
            for item in my_cpd_items:
                hours_logged_titles_list.append(item.title)
                hours_logged_values_list.append(item.hours_logged)
            data['success'] = True
            data['data'] = {
                "titles_data":hours_logged_titles_list,
                "hours_data":hours_logged_values_list
            }
            return Response(data,status=200)
        except Token.DoesNotExist:
            data["success"] = False
            data["message"] = "Invalid token"
            return Response(data, status=401)

@api_view(
    [
        "POST",
    ]
)
def create_cpd_plan(request):
    data = {}
    if request.method == "POST":
        token_key = request.headers.get("Authorization").split(" ")[1]
        token_object = Token.objects.get(key=token_key)
        user_object = token_object.user
        cpd_plan_title = request.data.get('cpd_plan_title')
        new_cpd_plan = CPDPlan.objects.create(
        status= "backlog",
        title = cpd_plan_title,
        user=user_object
        )
        cpd_plan_ser = CPDPlanSerializer(new_cpd_plan)
        data = cpd_plan_ser.data
        return Response(data, status=200)


@api_view(
    [
        "POST",
    ]
)
def change_cpd_plan_status(request):
    data = {}
    if request.method == "POST":
        token_key = request.headers.get("Authorization").split(" ")[1]
        token_object = Token.objects.get(key=token_key)
        user_object = token_object.user
        cpd_plan_id = request.data.get('cpd_plan_id')
        cpd_plan_status = request.data.get('cpd_plan_status')
        cpd_plan_object = CPDPlan.objects.get(id=cpd_plan_id,user=user_object)
        cpd_plan_object.status = cpd_plan_status
        cpd_plan_object.save()
        cpd_plan_ser = CPDPlanSerializer(cpd_plan_object)
        data = cpd_plan_ser.data
        return Response(data,status=200)

@api_view(
    [
        "GET",
    ]
)
def list_my_cpd_plans(request):
    data = {}
    if request.method == "GET":
        token_key = request.headers.get("Authorization").split(" ")[1]
        token_object = Token.objects.get(key=token_key)
        user_object = token_object.user
        cpd_plan_list = CPDPlan.objects.filter(user=user_object)
        cpd_plan_ser = CPDPlanSerializer(cpd_plan_list,many=True)
        data = cpd_plan_ser.data
        return Response(data,status=200)

@api_view(
    [
        "POST",
    ]
)
def delete_cpd_plan(request):
    data = {}
    if request.method == "POST":
        token_key = request.headers.get("Authorization").split(" ")[1]
        token_object = Token.objects.get(key=token_key)
        user_object = token_object.user
        cpd_plan_id = request.data.get('cpd_plan_id')
        cpd_plan_object = CPDPlan.objects.get(id=cpd_plan_id,user=user_object)
        cpd_plan_object.delete()
        data = {"message":"CPD Plan deleted"}
        return Response(data,status=200)


@api_view(
    [
        "GET",
    ]
)
def download_cpd_summary(request):
    data = {}
    if request.method == "GET":
        token_key = request.headers.get("Authorization").split(" ")[1]
        token_object = Token.objects.get(key=token_key)
        user_object = token_object.user
        the_path = os.path.join(BASE_DIR, "uploads")
        html_file_name = f"{user_object.first_name}_{user_object.last_name}_Cpd_summary.html"
        pdf_file_name = f"{user_object.first_name}_{user_object.last_name}_Cpd_summary.pdf"
                # Generate HTML content
        html_content = cpd_summary_html(request, user_object)
        
        # Save HTML content to a file
        with open(os.path.join(the_path, html_file_name), 'w') as html_file:
            html_file.write(html_content)
        HTML(os.path.join(the_path, html_file_name)).write_pdf(os.path.join(the_path, pdf_file_name))
        
        data = {
            "file_url": f"https://cpd-admin.apexnile.com/uploads/{pdf_file_name}"
                            }
        return Response(data,status=200)

def cpd_summary_html(request,user):
    cpd_items = CPDItem.objects.filter(user=user)
    hours_logged_list = list(cpd_items.values_list('hours_logged', flat=True))
    hours_logged_sum = sum(hours_logged_list)
    context = {"user": user,"cpd_items":cpd_items,"total_hours":hours_logged_sum}
    html_content = render_to_string("summary.html", context)
    return html_content