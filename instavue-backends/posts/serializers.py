# posts/serializers.py
from rest_framework import serializers
from .models import Post
from comments.models import Comment
from comments.serializers import CommentSerializer

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False)
    likes_count = serializers.SerializerMethodField()
   
    class Meta:
        model = Post
        fields = ['id', 'user', 'caption', 'image', 'created_at', 'comments']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        comments_data = validated_data.pop('comments', [])
        post = Post.objects.create(user=self.context['request'].user, **validated_data)

        for comment_data in comments_data:
            Comment.objects.create(post=post, user=self.context['request'].user, **comment_data)

        return post
    
    def get_likes_count(self, obj):
        return obj.likes.count()
