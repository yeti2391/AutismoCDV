from django.urls import path
from .views import CourseListView, CourseDetailView, VideoDetailView

app_name='content_app'

urlpatterns = [
    #path("course/", CourseListView.as_view(), name='course-list'),
    #path("course/<slug>/", CourseDetailView.as_view(), name='course-detail'), codigo origianl
    path("course/", CourseListView, name='course-list'),
    path("course/<slug>/", CourseDetailView, name='course-detail'),
    path("course/<slug>/<video_slug>", VideoDetailView.as_view(), name='video-detail')
]
