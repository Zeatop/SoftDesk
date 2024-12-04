from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Project.models import Contributor, Project
from Users.models import CustomUser as User
from Project.serializers import ProjectSerializer, ContributorSerializer


class Home(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    
class CreateProject(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = ProjectSerializer(data=request.data)

            name = request.data.get('name')
            if Project.objects.filter(name=name).exists():
                return Response({
                'message': 'Project already exist with same name',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
            if serializer.is_valid():
                project = serializer.save()
                
                Contributor.objects.create(
                    project=project,
                    user=request.user,
                    role='owner'
                )
                
                return Response({
                    'message': 'Project created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'message': 'Invalid data provided',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'message': 'An error occurred',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProjectViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=request.data)
        name = request.data.get('name')

        if Project.objects.filter(name=name).exists():
            return Response({
                'message': 'Project already exist with same name',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
                project = serializer.save()
                
                Contributor.objects.create(
                    project=project,
                    user=request.user,
                    role='owner'
                )
                return Response({
                    'message': 'Project created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
        

class AddContributor(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):

        project_id = request.data.get('project')
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response({
                    'message': 'Project not found'
                }, status=status.HTTP_404_NOT_FOUND)
        
        user = request.data.get('user')
        if User.objects.filter(pk=user):
            if not Contributor.objects.filter(
                    project=project, 
                    user=request.user, 
                    role='owner'
                ).exists():
                    return Response({
                        'message': 'Must be owner'
                    }, status=status.HTTP_403_FORBIDDEN)

            if Contributor.objects.filter(
                project=project,
                user=request.data.get('user')
            ).exists:
                return Response({
                        'message': 'Already a contributor'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            serializer = ContributorSerializer(data=request.data) 
            if serializer.is_valid():
                contributor = serializer.save()
                return Response({
                    'message': 'User added to project',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'message': 'Invalid data provided',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("error")
            
class AddContributor(viewsets.ViewSet):
    pass
