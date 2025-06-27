from django.urls import path
from .views import LikeListCreateView, LikeDetailView, ToggleLikeView

urlpatterns = [
    path('', LikeListCreateView.as_view(), name='like-list-create'),
    path('<int:pk>/', LikeDetailView.as_view(), name='like-detail'),
    path('toggle/<int:post_id>/', ToggleLikeView.as_view(), name='toggle-like'),
]
