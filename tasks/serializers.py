from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import serializers
from .models import Topic, Task, StudentTask, StudentTaskImage


class TopicSerializer(ModelSerializer):
    """
    Serializer for the Topic model.
    """
    class Meta:
        model = Topic
        fields = "__all__"


class TaskSerializer(ModelSerializer):
    """
    Serializer for the Task model.
    """
    class Meta:
        model = Task
        fields = "__all__"


class StudentTaskSerializer(ModelSerializer):
    """
    Serializer for the StudentTask model.
    """
    class Meta:
        model = StudentTask
        fields = "__all__"


class StudentTaskImageSerializer(ModelSerializer):
    """
    Serializer for the StudentTaskImage model.
    Handles the upload and validation of images.
    """
    class Meta:
        model = StudentTaskImage
        fields = "__all__"

    def validate_image(self, value):
        """
        Custom validation to check image file type and size.
        Ensures only jpg, jpeg, and png formats are allowed.
        Ensures that the image size does not exceed 10 MB.
        """
        if value.size > 10 * 1024 * 1024:
            raise ValidationError("Image size should not exceed 10 MB.")
        if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValidationError("Only .jpg, .jpeg, and .png formats are allowed.")
        return value



class StudentTaskSerializerV1(ModelSerializer):
    """
    Serializer for the StudentTask model.
    """
    images = StudentTaskImageSerializer(many=True, read_only=True, source='student_task_images')
    class Meta:
        model = StudentTask
        fields = "__all__"


class StudentTaskCreateSerializer(ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=True,
        help_text="Upload up to 200 images. Images should be .png or .jpg and not exceed 10MB each."
    )
    task_id = serializers.IntegerField(write_only=True, required=True, help_text="ID of the task")

    class Meta:
        model = StudentTask
        fields = ['task_id', 'images']

    def validate_images(self, images):
        if len(images) > 200:
            raise serializers.ValidationError("You can only upload up to 200 images.")
        return images

    def validate_task_id(self, task_id):
        if not Task.objects.filter(id=task_id).exists():
            raise serializers.ValidationError("Task with the given ID does not exist.")
        return task_id

    def create(self, validated_data):
        images = validated_data.pop('images')
        task_id = validated_data.pop('task_id')

        task = Task.objects.get(id=task_id)
        student = self.context['request'].user

        # Check if the student task already exists
        if StudentTask.objects.filter(student=student, task=task).exists():
            raise serializers.ValidationError("You have already submitted this task.")

        # Create the student task
        student_task = StudentTask.objects.create(student=student, task=task)

        # Handle image uploads
        image_instances = [
            StudentTaskImage(student_task=student_task, image=image) for image in images
        ]
        
        # Bulk create images
        StudentTaskImage.objects.bulk_create(image_instances)

        return student_task


class TaskWithStudentTaskSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'image', 'is_active', 'created_at', 'updated_at', 'status']

    def get_status(self, obj):
        # Get the authenticated user from context
        user = self.context['request'].user
        # Try to find the related StudentTask for the user and task
        try:
            student_task = StudentTask.objects.get(student=user, task=obj)
            return student_task.status
        except StudentTask.DoesNotExist:
            return None  # No related StudentTask, return null



class AllTaskWithStudentTaskSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'image', 'is_active', 'created_at', 'updated_at', 'status']

    def get_status(self, obj):
        # Get the authenticated user from context
        user = self.context['request'].user
        # Try to find the related StudentTask for the user and task
        try:
            student_task = StudentTask.objects.get(student=user)
            return student_task.status
        except StudentTask.DoesNotExist:
            return None  # No related StudentTask, return null