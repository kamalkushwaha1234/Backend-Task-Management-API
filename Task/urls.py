from django.urls import path
from .views import getCerateOrRetiveTask,getUpdateOrDelateOrRetiveTask

urlpatterns = [
    path('',getCerateOrRetiveTask, name='Cerate Or Retive Task'),
    path('<str:pk>/',getUpdateOrDelateOrRetiveTask, name='Update Or Delate Or Retive Task'),
 
   
] 