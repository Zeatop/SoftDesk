from django.urls import path
from .views import Home, CreateProject, AddContributor


urlpatterns = [
    path('', Home.as_view()),
    path('createproject', CreateProject.as_view()),
    # path('addcontributor', AddContributor.as_view()),
] 