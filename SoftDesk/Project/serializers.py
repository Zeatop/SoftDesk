from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'devType', 'deviceType']

    def validate_name(self, data):
        if Project.objects.filter(name=data.name).exists():
            raise serializers.ValidationError("Un projet porte déjà ce nom")
        return data


class IssueSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    #Permet de faire le lien entre l'ID du projet et son name
    project = serializers.SlugRelatedField(
        queryset=Project.objects.all(),
        slug_field='name'
    )

    class Meta: 
        model = Issue
        fields = ['id', 'name', 'priority', 'balise', 'state', 'project', "author" ]
    
    def validate(self, data):
        """
        Vérifie que l'auteur est bien contributeur du bon projet
        """
        project = data.get('project')
        issue = data.get('name')
        request = self.context.get('request')

        if not request or not request.user:
            raise serializers.ValidationError("Requête invalide")
        
        try:
            contributor = Contributor.objects.get(
            project=project,
            user=request.user
            )
        except Contributor.DoesNotExist:
            raise serializers.ValidationError(
            "Vous devez être contributeur pour créer une issue"
        )
    
        if self.instance:
            is_author = (self.instance.author.user == request.user)
            is_owner = (contributor.role == 'owner')
            
            if not (is_author or is_owner):
                raise serializers.ValidationError(
                    "Seuls l'owner du projet et l'auteur de l'issue peuvent la modifier"
                )
        else:
            if Issue.objects.filter(project=project, name=issue).exists():
                raise serializers.ValidationError(
                    "Une issue porte déjà ce nom dans ce projet"
                )

        return data
     


class CommentSerializer(serializers.ModelSerializer):
    issue = serializers.SlugRelatedField(
        queryset=Issue.objects.all(),
        slug_field='name'
    )
    class Meta: 
        model = Comment
        fields = ['id', 'issue', 'body', 'author']

    def validate(self, data):
        """
        Vérifie que l'auteur est bien contributeur du bon projet
        """
        issue = data.get('issue')
        project = issue.project
        request = self.context.get('request')
        user = request.user

        if not request or not request.user:
         raise serializers.ValidationError("Requête invalide")
        try:
            Contributor.objects.get(
                user=user,
                project=project
            )
        except Contributor.DoesNotExist:
            raise serializers.ValidationError(
                "L'auteur doit être contributeur du projet"
            )
        
         # Pour les modifications
        if self.instance:
            author = self.instance.author
            contributor = Contributor.objects.get(
                project=project,
                user=request.user
            )
            
            is_author = (author == contributor)
            if not (is_author):
                raise serializers.ValidationError(
                    "Seul l'auteur du commentaire du projet peut modifier le commentaire"
                )

        return data
    

class ContributorSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Contributor
        fields = ['id', 'project', 'user', 'date_joined', 'role' ]

    def validate(self, data):
        if Contributor.objects.filter(user=data.user, projet=data.projet).exists():
            raise serializers.ValidationError("Un projet porte déjà ce nom")
        if not Project.objects.filter(pk=data.project).exists:
            raise serializers.ValidationError("Le projet n'existe pas")
        return data