from django.urls import path
from .views import FollowUserView, UnfollowUserView, MyFollowersListView, MyFollowingListView

urlpatterns = [
    path('follow/', FollowUserView.as_view(), name='follow'),
    path('unfollow/', UnfollowUserView.as_view(), name='unfollow'),
    path('followers/', MyFollowersListView.as_view(), name='followers'),
    path('following/', MyFollowingListView.as_view(), name='following'),
]
