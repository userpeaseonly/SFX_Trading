from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import StudentTask, StudentTaskImage, Task
from .serializers import StudentTaskSerializer, StudentTaskCreateSerializer


class StudentTaskListView(generics.ListAPIView):
    """
    API view to retrieve all student tasks for the authenticated user.
    """
    serializer_class = StudentTaskSerializer
    

    def get_queryset(self):
        """
        Filter the student tasks by the authenticated user (student).
        """
        return StudentTask.objects.filter(student=self.request.user)


class StudentTaskDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a specific student task by task_id for the authenticated user.
    """
    serializer_class = StudentTaskSerializer

    def get_object(self):
        """
        Override to ensure that the student task belongs to the authenticated user.
        """
        task_id = self.kwargs['task_id']
        task = get_object_or_404(Task, id=task_id)
        return get_object_or_404(StudentTask, student=self.request.user, task=task)


class StudentTaskCreateAPIView(generics.CreateAPIView):
    """
    API view to create a new student task and upload images.
    """
    serializer_class = StudentTaskCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_task = serializer.save()

        return Response({
            "student_task_id": student_task.id,
            "message": "Student task submitted successfully",
            "images_uploaded": len(request.FILES.getlist('images'))
        }, status=status.HTTP_201_CREATED)