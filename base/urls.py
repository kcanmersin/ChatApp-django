from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('search/', views.searchPage, name="search"),
    path('edit-profile/', views.editProfilePage, name="edit-profile"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('chat-room/<str:pk>/', views.chatPage, name="chat-room"),


    path('follow/<str:pk>/', views.follow, name='follow'),
    path('unfollow/<str:pk>/', views.unfollow, name='unfollow'),

    path('', views.home, name="home"),

]
