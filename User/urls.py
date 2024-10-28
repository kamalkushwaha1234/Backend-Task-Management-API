#user_URLS.py

from django.urls import path
from .views import registerUser,MyTokenObtainPairView


urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/',registerUser, name="register"),
]