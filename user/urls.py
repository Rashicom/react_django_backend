from django.urls import path, include
from .import views

urlpatterns = [
    path('signup/', views.signup.as_view()),
    path('login/', views.login.as_view()),
    path('home/', views.home.as_view()),
    path('update_image/', views.update_image.as_view())
    
]
