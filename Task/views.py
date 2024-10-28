from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters
from .serializers import TaskSerializer
from .models import Task
from .filters import TaskFilter 
from rest_framework.pagination import PageNumberPagination


class TaskPagination(PageNumberPagination):
    page_size = 10

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getCerateOrRetiveTask(request):
    if request.method == 'GET':
       
        tasks = Task.objects.filter(created_by=request.user)
        
        
        filtered_tasks = TaskFilter(request.GET, queryset=tasks).qs

        
        ordering = request.query_params.get('ordering', None)
        if ordering:
            filtered_tasks = filtered_tasks.order_by(ordering)

        
        paginator = TaskPagination()
        paginated_tasks = paginator.paginate_queryset(filtered_tasks, request)

        
        serializer = TaskSerializer(paginated_tasks, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def getUpdateOrDelateOrRetiveTask(request, pk):
    try:
        
        task = Task.objects.get(pk=pk, created_by=request.user)
    except Task.DoesNotExist:
        return Response({"detail": "Task not found or you do not have permission to access it."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
