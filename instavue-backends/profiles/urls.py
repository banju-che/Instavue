from django.urls import path
from .views import MyProfileView, PublicProfileByIDView, PublicProfileByUsernameView, SearchUserView


urlpatterns = [
    path('me/', MyProfileView.as_view(), name='my-profile'),
    path('user/id/<int:user__id>/', PublicProfileByIDView.as_view(), name='profile-by-id'),
    path('user/username/<str:user__username>/', PublicProfileByUsernameView.as_view(), name='profile-by-username'),
    path('search/', SearchUserView.as_view(), name='search-users'),
]
