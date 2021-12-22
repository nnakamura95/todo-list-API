from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView

urlpatterns = [
    path('', TaskListCreateView.as_view()),
    path('<int:pk>/', TaskRetrieveUpdateDestroyView.as_view()),
]
