from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('signup/', views.signupPage, name='signup'),
    path('logout/', views.logoutCurrentUser, name='logout'),
    path('profile/', views.profilePage, name='profile'),
    path('searchhistory/', views.searchHistoryPage, name='searchhistory'),
]