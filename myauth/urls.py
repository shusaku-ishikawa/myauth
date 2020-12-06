from django.urls import path, include
from myauth import views

app_name = 'myauth'
urlpatterns = [
    path('', views.Login.as_view(), name = 'login'),
    path('logout/', views.Logout.as_view(), name = 'logout'),
    path('top/', views.Top.as_view(), name = 'top'),
    path('signup/', views.SignUp.as_view(), name = 'add_user'),
    path('users/', views.ListUser.as_view(), name = 'list_user'),
    path('users/<str:pk>', views.Profile.as_view(), name = 'profile'),
    path('users/<str:pk>/delete', views.DeleteUser.as_view(), name = 'delete_user'),
    path('users/<str:pk>/change-password', views.ChangePassword.as_view(), name='change_password')
]