from django.contrib import admin
from django.urls import path, include
from newsapp.views import HomeView, UserRegistrationView, UserLoginView, UserDashboard, UserLogout


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user-dashboard/', UserDashboard.as_view(), name='dashboard'),
    path('logout/', UserLogout.as_view(), name='logout')


]
