from django.urls import path, include
from .views import Home, ProjectViewSet, IssueViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# Enregistrer les ViewSets dans le routeur
# Le premier argument est le préfixe de l'URL, le second est le ViewSet
router.register('projects', ProjectViewSet, basename='project')
router.register('issues', IssueViewSet, basename='issue')
router.register('comments', CommentViewSet, basename='comment')

# Créer la liste des URLs
urlpatterns = [
    # Inclure toutes les URLs générées par le routeur
    
]
urlpatterns = [
    path('', Home.as_view()),
    path('', include(router.urls)),

] 