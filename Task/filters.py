from django_filters import rest_framework as filters
from .models import Task

class TaskFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=Task.STATUS_CHOICES)
    priority = filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES)
    due_date = filters.DateFromToRangeFilter()

    class Meta:
        model = Task
        fields = ['title', 'status', 'priority', 'due_date']
