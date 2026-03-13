from django.urls import path
from . import views

app_name = 'forums'

urlpatterns = [
    path('faculties/', views.FacultyListView.as_view(), name='faculty_list'),
    path('faculties/<str:short_name>/', views.FacultyFeedView.as_view(), name='faculty_feed'),
    path('faculties/<str:short_name>/<slug:slug>/', views.ForumDetailView.as_view(), name='forum_detail'),
    path('threads/<slug:slug>/', views.ThreadDetailView.as_view(), name='thread_detail'),
    path('replies/<int:pk>/delete/', views.ReplyDeleteView.as_view(), name='reply_delete'),
    path('threads/<slug:slug>/delete/', views.ThreadDeleteView.as_view(), name='thread_delete'),
    path('vote/<str:model_type>/<int:pk>/<str:action>/', views.VoteView.as_view(), name='vote'),
]