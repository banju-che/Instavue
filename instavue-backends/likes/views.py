from rest_framework import generics, permissions, status
from .models import Like
from rest_framework.views import APIView
from rest_framework.response import Response
from posts.models import Post
from .serializers import LikeSerializer

class LikeListCreateView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeDetailView(generics.RetrieveDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ToggleLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        user = request.user
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=user, post=post)

        if not created:
            # Already liked: remove (unlike)
            like.delete()
            return Response({"message": "Unliked"}, status=status.HTTP_200_OK)

        return Response({"message": "Liked"}, status=status.HTTP_201_CREATED)