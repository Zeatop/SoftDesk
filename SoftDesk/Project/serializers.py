from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'devType', 'deviceType']

    def validate_name(self, value):
        if Project.objects.filter(name=value).exists():
            raise serializers.ValidationError("Un projet porte déjà ce nom")
        return value


class IssueSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Issue
        fields = ['id', 'name', 'priority', 'balise', 'state', 'project', ]
    
    def validate(self, data):
        """
        Vérifie que l'auteur est bien contributeur du bon projet
        """
        project = data.get('project')
        issue = data.get('name')
        author = data.get('author')
        request = self.context.get('request')
        
        if request and request.user:
            # Vérifie si l'utilisateur actuel est contributeur
            if not Contributor.objects.filter(
                project=project,
                user=request.user
            ).exists():
                raise serializers.ValidationError(
                    "Vous devez être contributeur de ce projet pour créer une issue"
                )
        
            return data
        
        if self.instance:
            is_author = (author == self.instance.author)
            is_owner = project.contributors.filter(user=author.user, role='owner').exists()
            
            if not (is_author or is_owner):
                raise serializers.ValidationError(
                    "Seuls l'owner du projet et l'auteur de l'issue peuvent la modifier"
                )
        else:
            if Issue.objects.filter(name=issue).exists():
                raise serializers.ValidationError(
                    "Une issue porte déjà ce nom"
                )

        return data
    
    


class CommentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Comment
        fields = ['id', 'issue', 'body', 'author']

    def validate(self, data):
        """
        Vérifie que l'auteur est bien contributeur du bon projet
        """
        issue = data.get('issue')
        project = issue.project
        author = data.get('author')
        
        if author not in project.contributors.all():
            raise serializers.ValidationError(
                "L'auteur doit être contributeur de ce projet spécifique"
            )
        
        if self.instance:
            is_author =(author == self.instance.author)
            if not is_author:
                raise serializers.ValidationError(
                    "Seul l'auteur du commentaire peut modifier le commentaire"
                )
        return data
    

class ContributorSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Contributor
        fields = ['id', 'project', 'user', 'date_joined', 'role' ]