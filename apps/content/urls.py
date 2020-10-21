from django.urls import path
from .views import CourseListView, CourseDetailView, VideoDetailView, ProductListView, ProductDetailView

app_name='content_app'

urlpatterns = [
    path("product/", ProductListView.as_view(), name='product-list'),
    path("product/<slug>/", ProductDetailView.as_view(), name='product-detail'),
    path("course/", CourseListView, name='course-list'),
    path("course/<slug>/", CourseDetailView, name='course-detail'),
    path("course/<slug>/<video_slug>", VideoDetailView.as_view(), name='video-detail')
]
