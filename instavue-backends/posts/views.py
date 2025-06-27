from .serializers import PostSerializer
from rest_framework import generics
from .models import Post
from .permissions import IsPostOwnerOrAdminMod

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsPostOwnerOrAdminMod]