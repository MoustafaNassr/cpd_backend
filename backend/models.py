from django.db import models
from  django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    profile_image = models.FileField(upload_to="uploads/")
    profession_title = models.CharField(max_length=200)
    user = models.ForeignKey(User,related_name="profile",on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.email}"
class SkillArea(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
class FormatOfTraining(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.name}"

class CPDItem(models.Model):
    type_choices = (
        ("Formal Learning","Formal Learning"),
        ("Self-directed study","Self-directed study"),
        ("Contributing to the profession","Contributing to the profession"),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    type= models.CharField(max_length=250,choices=type_choices)
    skills_area =  models.ForeignKey(SkillArea,on_delete=models.PROTECT)
    format_of_training = models.ForeignKey(FormatOfTraining,on_delete=models.PROTECT)
    hours_logged = models.PositiveIntegerField()
    date_completed = models.DateField()
    cost_of_cpd = models.PositiveIntegerField()
    what_did_you_learn = models.TextField(null=True,blank=True)
    future_dev_notes = models.TextField(null=True,blank=True)
    # file  = models.FileField(upload_to="uploads/")

    def __str__(self) -> str:
        return f"{self.title}" 
    
class CPDPlan(models.Model):
    status_choices = (
            ("backlog","backlog"),
            ("todo","todo"),
            ("in_progress","in_progress"),
            ("complete","complete"),
        )
    status = models.CharField(choices=status_choices,max_length=120)
    title = models.CharField(max_length=120)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title}"