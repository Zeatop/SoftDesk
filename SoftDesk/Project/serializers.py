from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'devType', 'deviceType']

class IssueSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Issue
        fields = ['id', 'priority', 'balise', 'state', 'project', 'author' ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Comment
        fields = ['id', 'issue', 'body', 'author']

class ContributorSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Contributor
        fields = ['id', 'project', 'user', 'date_joined', 'role' ]