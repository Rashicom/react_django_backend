from django.urls import path, include
from .import views

urlpatterns = [
    path('login/', views.login.as_view()),
    path('user_list/',views.users_list.as_view()),
    path('add_user/',views.add_user.as_view()),
    path('delete_user/<str:user_id>', views.delete_user.as_view()),
    path('update_user/',views.update_user.as_view())
    
]