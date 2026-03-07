from django.urls import path
from . import views

app_name = 'forums'

urlpatterns = [
    path('faculties/', views.FacultyListView.as_view(), name='faculty_list'),
    path('faculties/<str:short_name>/', views.FacultyFeedView.as_view(), name='faculty_feed'),
    path('faculties/<str:short_name>/<slug:slug>/', views.ForumDetailView.as_view(), name='forum_detail'),
]