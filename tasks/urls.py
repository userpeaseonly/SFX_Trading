# urls.py
from django.urls import path
from .safe_views import TopicListView, TopicDetailView, TopicTasksListView, StudentCountTaskStatusView, TopicTasksWithStudentTasksView, AllTopicTasksWithStudentTasksView
from .student_task_views import StudentTaskListView, StudentTaskDetailView, StudentTaskDetailViewV1, StudentTaskCreateAPIView


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

    # Retrieve a specific student task by task_id for the authenticated user
    path('student-tasks/<int:task_id>/v1/', StudentTaskDetailViewV1.as_view(), name='student-task-detail'),

    # Create a new student task with image uploads
    path('student-tasks/submit/', StudentTaskCreateAPIView.as_view(), name='student-task-create'),

    # Student tasks
    path('count-status/', StudentCountTaskStatusView.as_view(), name='student-task-count-status'),

    # Get all topics with tasks and student tasks
    path('topics/<int:id>/tasks-with-student-tasks/', TopicTasksWithStudentTasksView.as_view(), name='tasks-with-student-tasks'),
    
    # Get all topics with tasks and student tasks
    path('topics/tasks-with-student-tasks/', AllTopicTasksWithStudentTasksView.as_view(), name='tasks-with-student-tasks'),
]
