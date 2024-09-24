# urls.py
from django.urls import path
from .safe_views import TopicListView, TopicDetailView, TopicTasksListView
from .student_task_views import StudentTaskListView, StudentTaskDetailView, StudentTaskCreateAPIView


urlpatterns = [
    # GET all topics
    path('topics/', TopicListView.as_view(), name='topic-list'),

    # GET a specific topic by id
    path('topics/<int:id>/', TopicDetailView.as_view(), name='topic-detail'),

    # GET all tasks for a specific topic
    path('topics/<int:id>/tasks/', TopicTasksListView.as_view(), name='topic-tasks'),
    
    # Get all student tasks for the authenticated user
    path('student-tasks/', StudentTaskListView.as_view(), name='student-task-list'),

    # Retrieve a specific student task by task_id for the authenticated user
    path('student-tasks/<int:task_id>/', StudentTaskDetailView.as_view(), name='student-task-detail'),

    # Create a new student task with image uploads
    path('student-tasks/submit/', StudentTaskCreateAPIView.as_view(), name='student-task-create'),
    
]
