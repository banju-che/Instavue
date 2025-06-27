from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


# 🔓 Public profile by user ID
class PublicProfileByIDView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'user__id'  # Custom field for lookup


# 🔓 Public profile by username
class PublicProfileByUsernameView(generics.RetrieveAPIView):
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'user__username'

class SearchUserView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Profile.objects.select_related('user').filter(
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(bio__icontains=query)
        )