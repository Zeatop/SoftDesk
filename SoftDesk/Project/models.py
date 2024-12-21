from datetime import datetime
from django.db import models
from django.contrib.auth import models as modelsAuth
from Users.models import CustomUser
from rest_framework.response import Response
from rest_framework import status


class Project(models.Model):
    DEVTYPE = [
        ("Backend", "Backend"),
        ("Frontend", "Frontend"),
    ]
    DEVICE = [
        ("iOS", "iOS"),
        ("Android", "Android"),
    ]

    name = models.CharField(max_length=25, null=True)
    description = models.CharField(max_length=200, null=False)
    devType = models.CharField(max_length=50, null=False, choices=DEVTYPE)
    deviceType = models.CharField(max_length=50, null=False, choices=DEVICE)
    contributors = models.ManyToManyField(
        CustomUser,
        through='Contributor',
        through_fields=('project', 'user'),
        related_name='projects'
    )
    
    def join(self, user):
        return Contributor.objects.create(
            project=self,
            user=user,
            role='contributor'  # Par défaut, on assigne le rôle contributeur
        )   
    

class Contributor(models.Model):
    ROLE=[
            ('owner', 'Project Owner'),
            ('contributor', 'Contributor'),
        ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    role = models.CharField(max_length=30, choices=ROLE, default='contributor')
    
    class Meta:
        unique_together = ('project', 'user')  # Pour éviter les doublons


class Issue(models.Model):
    PRORITY = [
        ("Low", "Low"),
        ("Med", "Med"),
        ("High", "High")
    ]
    TAG = [
        ("Fix", "Fix"),
        ("Task", "Task"),
        ("Upgrade", "Upgrade")
    ]
    STATE = [
        ("To do", "To do"),
        ("In progress", "In progress"),
        ("Finished", "Finished")
    ]

    name = models.CharField(max_length=25, null=True)
    priority = models.CharField(max_length=50, null=False, choices=PRORITY)
    balise = models.CharField(max_length=50, null=False, choices=TAG)
    state = models.CharField(max_length=50, null=False, choices=STATE, default="To do")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE)

class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    body = models.CharField(max_length=200, null=False)
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE)