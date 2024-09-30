from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .validators import validate_image

class Topic(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'), unique=True)
    description = models.TextField(verbose_name=_('Description'))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')


class Task(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='tasks', verbose_name=_('Topic'))
    title = models.CharField(max_length=255, verbose_name=_('Title'), unique=True)
    description = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to='task_images/', validators=[validate_image], verbose_name=_('Image'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class StudentTask(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        REJECTED = 'Rejected', _('Rejected')
        APPROVED = 'Approved', _('Approved')
    student = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='student_tasks', verbose_name=_('Student'))
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='student_tasks', verbose_name=_('Task'))
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name=_('Status')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    
    def __str__(self):
        return f"{self.student} - {self.task}"

    def get_absolute_url(self):
        return reverse('admin:studenttaskimage_changelist', args=[self.id])
    
    class Meta:
        unique_together = ('student', 'task')
        verbose_name = _('Student Task')
        verbose_name_plural = _('Student Tasks')
    
    def completed_tasks(self):
        return StudentTask.objects.filter(student=self.student, status=StudentTask.StatusChoices.APPROVED).count()
        
class StudentTaskImage(models.Model):
    student_task = models.ForeignKey(StudentTask, on_delete=models.CASCADE, related_name='student_task_images', verbose_name=_('Student Task'))
    image = models.ImageField(upload_to='student_task_images/', validators=[validate_image], verbose_name=_('Image'))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Uploaded At'))

    def __str__(self):
        return f"StudentTaskImage {self.student_task}"
    
    class Meta:
        verbose_name = _('Student Task Image')
        verbose_name_plural = _('Student Task Images')
        