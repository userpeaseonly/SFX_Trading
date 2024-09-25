from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.urls import reverse
from .models import Topic, Task, StudentTask, StudentTaskImage

# Registering the admin views with optimal configurations for scalability and performance.


# ------------------------------
# Inline Admin for Task under Topic
# ------------------------------
class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

    def has_delete_permission(self, request, obj=None):
        # Ensure that obj is an instance of Task before querying StudentTask
        if obj and not isinstance(obj, Task):
            return False

        # Prevent deletion if StudentTask objects exist for the Task
        if obj and StudentTask.objects.filter(task=obj).exists():
            return False

        return True


# ------------------------------
# Topic Admin
# ------------------------------
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    list_filter = ['name']
    inlines = [TaskInline]  # Allow adding/editing tasks directly from the Topic page

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('tasks')  # Prefetch to optimize related tasks loading

    class Media:
        css = {
            'all': ('admin/custom.css',)  # Include custom CSS for styling if needed
        }


# ------------------------------
# StudentTaskImage Inline Admin
# ------------------------------
class StudentTaskImageInline(admin.TabularInline):
    model = StudentTaskImage
    extra = 0  # No extra fields by default
    readonly_fields = ['uploaded_at', 'display_image']
    fields = ['image', 'display_image', 'uploaded_at']
    can_delete = True

    # Display the uploaded image in the admin panel.
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 150px; max-height: 150px;" />', obj.image.url)
        return _("No Image")

    display_image.short_description = _('Uploaded Image')


# ------------------------------
# Task Admin
# ------------------------------
# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ['title', 'description', 'topic', 'is_active', 'created_at', 'updated_at']
#     search_fields = ['title', 'description', 'topic__name']
#     list_filter = ['is_active', 'topic', 'created_at']
#     readonly_fields = ['created_at', 'updated_at']
#     ordering = ['-created_at']

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         return queryset.select_related('topic')  # Optimize queryset by selecting related topic


# ------------------------------
# StudentTask Admin
# ------------------------------
@admin.register(StudentTask)
class StudentTaskAdmin(admin.ModelAdmin):
    list_display = ['student', 'task', 'status', 'created_at', 'updated_at', 'view_images_link']
    list_filter = ['status', 'task__topic', 'created_at']
    search_fields = ['student__full_name', 'task__title']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [StudentTaskImageInline]  # Show images related to the task inline

    def view_images_link(self, obj):
        # Use a specific URL for images, you can define this according to your project structure
        url = reverse('admin:tasks_studenttaskimage_changelist') + f'?student_task__id__exact={obj.id}'
        return format_html('<a href="{}">View {} Images</a>', url, obj.student_task_images.count())

    view_images_link.short_description = 'View Images'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('student', 'task').prefetch_related('student_task_images')  # Optimize queryset


# ------------------------------
# StudentTaskImage Admin
# ------------------------------
@admin.register(StudentTaskImage)
class StudentTaskImageAdmin(admin.ModelAdmin):
    list_display = ['student_task', 'uploaded_at', 'image_preview']
    list_filter = ['uploaded_at']
    search_fields = ['student_task__student__full_name', 'student_task__task__title']
    readonly_fields = ['uploaded_at', 'image_preview']

    # Display a preview of the uploaded image.
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.image.url)
        return _("No Image")

    image_preview.short_description = _('Preview')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('student_task__student', 'student_task__task')  # Optimize queryset
