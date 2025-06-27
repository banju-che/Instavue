from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Follow
from .serializers import FollowSerializer, CustomUserSerializer

User = get_user_model()

class FollowUserView(APIView):
    permission_classes = [permissions.isAuthenticated]
    
    def post(self,request):
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"detail": "user_id is required"}, status=400)
        
        if user_id == request.user.id:
            return Response({"detail": "You cannot follow yourself."}, status=400)
            
        try:
            following = User.objects.get(id=user_id)
            follow, created = Follow.objects.get_or_create(follower=request.user, following=following)

            if not created:
                return Response({"detail": "You are already following this user."}, status=400)

            return Response({"detail": "Started following successfully."}, status=201)


        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"detail": "user_id is required"}, status=400)

        try:
            following = User.objects.get(id=user_id)
            follow = Follow.objects.filter(follower=request.user, following=following)

            if follow.exists():
                follow.delete()
                return Response({"detail": "You have unfollowed successfully."})
            else:
                return Response({"detail": "You are not following this user."}, status=400)

        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

    
class MyFollowersListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user)


class MyFollowingListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    