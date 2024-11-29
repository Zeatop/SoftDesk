from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Project.models import Contributor
from Project.serializers import ProjectSerializer


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
