from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model
from follow.models import Follow

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField() 

    class Meta:
        model = Profile
        fields = [
            'id', 'username', 'email', 'bio', 'location', 'profile_picture',
            'date_of_birth', 'follower_count', 'following_count', 'is_following',
        ]

    def get_follower_count(self, obj):
        return Follow.objects.filter(following=obj.user).count()

    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj.user).count()

    def get_is_following(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        # Current user follows this profile's user?
        return Follow.objects.filter(follower=request.user, following=obj.user).exists()