from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Project.models import Contributor, Project, Issue
from Users.models import CustomUser as User
from Project.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer


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
        if serializer.is_valid():
                project = serializer.save()
                Contributor.objects.create(
                    project=project,
                    user=self.request.user,
                    role='owner'
                )
                return Response({
                    'message': 'Projet créé.',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response({
        'message': 'Projet non créé, données invalides.',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """
        Permet à un utilisateur authentifié de rejoindre un projet spécifique.
        accessible via POST /projects/{id}/join/
        """
        project = self.get_object()  # Récupère le projet via son ID (pk)

        # Vérifie si l'utilisateur est déjà contributeur
        if Contributor.objects.filter(project=project, user=request.user).exists():
            return Response({
                'message': 'Vous êtes déjà contributeur de ce projet.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Crée un nouveau contributeur
            contributor = Contributor.objects.create(
                project=project,
                user=request.user,
                role='contributor'  # Par défaut, on assigne le rôle contributeur
            )
            
            # Sérialise le contributeur pour la réponse
            serializer = ContributorSerializer(contributor)
            
            return Response({
                'message': 'Vous avez rejoint le projet avec succès.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'message': 'Une erreur est survenue lors de l\'ajout au projet.',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        
        project = serializer.validated_data['project']
        try:
            author = Contributor.objects.get(
                project=project,
                user=self.request.user
            )
            # Sauvegarder l'issue avec l'auteur trouvé automatiquement
            serializer.save(author=author)
            return Response({
                'message': 'Issue créée.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except Contributor.DoesNotExist:
            return Response({
                'message': 'Vous devez être contributeur du projet pour créer une issue.',
            }, status=status.HTTP_403_FORBIDDEN)
    


class CommentViewSet(viewsets.ModelViewSet):
     pass