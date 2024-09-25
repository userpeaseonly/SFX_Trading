from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Topic, Task
from .serializers import TopicSerializer, TaskSerializer


class TopicListView(generics.ListAPIView):
    """
    API view to retrieve all topics.
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]


class TopicDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a specific topic by its id.
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


class TopicTasksListView(generics.ListAPIView):
    """
    API view to retrieve all tasks for a given topic.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override this method to get tasks related to a specific topic.
        """
        topic_id = self.kwargs.get("id")
        topic = get_object_or_404(Topic, id=topic_id)
        return Task.objects.filter(topic=topic)

    def list(self, request, *args, **kwargs):
        """
        Override to return a custom response with topic details and its tasks.
        """
        response_data = super().list(request, *args, **kwargs).data
        topic = get_object_or_404(Topic, id=self.kwargs.get("id"))
        topic_data = TopicSerializer(topic).data
        topic_data["tasks"] = response_data
        return Response(topic_data, status=status.HTTP_200_OK)

