from datetime import datetime
from django.db import models
from django.contrib.auth import models as modelsAuth
from Users.models import CustomUser

class Project(models.Model):
    devChoice = [
        ("Backend", "Backend"),
        ("Frontend", "Frontend"),
    ]
    deviceChoice = [
        ("iOS", "iOS"),
        ("Android", "Android"),
    ]

    description = models.CharField(max_length=200, null=False)
    devType = models.CharField(max_length=50, null=False, choices=devChoice)
    deviceType = models.CharField(max_length=50, null=False, choices=deviceChoice)
    contributors = models.ManyToManyField(
        CustomUser,
        through='Contributor',
        through_fields=('project', 'user'),
        related_name='projects'
    )

class Contributor(models.Model):
    roleChoices=[
            ('owner', 'Project Owner'),
            ('contributor', 'Contributor'),
        ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    role = models.CharField(max_length=30, choices=roleChoices, default='contributor')

    
    class Meta:
        unique_together = ('project', 'user')  # Pour éviter les doublons

class Issue(models.Model):
    priorityChoice = [
        ("Low", "Low"),
        ("Med", "Med"),
        ("High", "High")
    ]
    baliseChoice = [
        ("Fix", "Fix"),
        ("Task", "Task"),
        ("Upgrade", "Upgrade")
    ]
    stateChoice = [
        ("To do", "To do"),
        ("In progress", "In progress"),
        ("Finished", "Finished")
    ]

    priority = models.CharField(max_length=50, null=False, choices=priorityChoice)
    balise = models.CharField(max_length=50, null=False, choices=baliseChoice)
    state = models.CharField(max_length=50, null=False, choices=stateChoice, default="To do")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    body = models.CharField(max_length=200, null=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)