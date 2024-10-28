from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User 

# Create your models here.
class Task(models.Model):

    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in-progress'
    STATUS_COMPLETE = 'complete'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETE, 'Complete'),
    ]
    
    PRIORITY_LOW = 'low'
    PRIORITY_HIGH = 'high'
    
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_HIGH, 'High'),
    ]

    title=models.CharField(max_length=100,blank=False,null=False)
    description=models.TextField(null=True,blank=True)
    status=models.CharField(max_length=100, choices=STATUS_CHOICES,blank=False,null=False)
    priority=models.CharField(max_length=100, choices=PRIORITY_CHOICES, blank=False,null=False)
    due_date=models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def validations (self):
        if self.due_date and self.due_date< timezone.now().date():
            raise ValidationError("Due date cannot be in the past.")

        if self.pk:  # Only check status transitions if the task already exists

            previous_status = Task.objects.get(pk=self.pk).status
            if previous_status == self.STATUS_PENDING and self.status == self.STATUS_COMPLETE:
                raise ValidationError("Cannot transition directly from 'Pending' to 'Complete'.")
            elif previous_status == self.STATUS_IN_PROGRESS and self.status == self.STATUS_PENDING:
                raise ValidationError("Cannot transition from 'In Progress' back to 'Pending'.")
    
    def save(self, *args, **kwargs):
        self.validations()
        super().save(*args, **kwargs)

    def __str__ (self):
        return f"{self.title} ----------- {self.status.upper() if self.status else ''}"