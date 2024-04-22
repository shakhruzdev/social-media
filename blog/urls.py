from django.urls import path
from .views import (
    index_view, upload_view,
    follow_view, like_view,
    profile_settings_view,
    search_view, profile_view
)

urlpatterns = [
    path('', index_view),
    path('upload/', upload_view),
    path('follow/', follow_view),
    path('like/<int:pk>', like_view, name='post_like'),
    path('settings/<int:pk>/', profile_settings_view),
    path('search/', search_view),
    path('profile/', profile_view, name='profile'),
]
