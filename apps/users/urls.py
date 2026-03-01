from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.CustomSignupView.as_view(), name='signup'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
]