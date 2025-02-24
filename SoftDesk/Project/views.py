from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Project.models import Contributor, Project, Issue, Comment
from Users.models import CustomUser as User
from Project.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer


class Home(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):       
        project = serializer.save()
        Contributor.objects.create(
            project=project,
            user=self.request.user,
            role='owner'
        )

    @action(detail=True, methods=['post'])
    def join(self, request, *args, **kwargs):
        """
        Permet à un utilisateur authentifié de rejoindre un projet spécifique.
        accessible via POST /projects/join/
        """
        user = request.user
        project = self.get_object()
        if Contributor.objects.filter(project=project, user=user).exists():
            return Response({"detail": "Vous êtes déjà contributeur de ce projet"}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
        # Utiliser directement la méthode join du modèle Project
        contributor = project.join(user)
        
        # Sérialiser le résultat
        serializer = ContributorSerializer(contributor)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            

class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        #is_valide
        project = serializer.validated_data['project']
        author = Contributor.objects.get(
        project=project,
        user=self.request.user
        )
        serializer.save(author=author)
        
    


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        issue = serializer.validated_data['issue']
        project = issue.project
        author = Contributor.objects.get(
                project=project,
                user=self.request.user
            )
        serializer.save(author=author)


