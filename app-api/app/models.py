from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings


class Task(models.Model):
    class TaskObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='active')

    options = (
        ('active', 'active'),
        ('completed', 'completed'),
    )

    task_name = models.CharField(max_length=200)
    comments = models.TextField(null=True, blank=True, default='')
    status = models.CharField(max_length=10, choices=options, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task')
    objects = models.Manager()  # default manager
    taskobjects = TaskObjects()  # custom manager

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.task_name
