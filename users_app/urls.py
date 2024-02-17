from django.urls import path
from users_app import views


# app_name = 'users_app'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profileEd/', views.profile_editor, name='profile_editor'),

]