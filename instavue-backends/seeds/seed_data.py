# seeds/seed_data.py

from django.contrib.auth import get_user_model
from posts.models import Post
from follow.models import Follow
from profiles.models import Profile
from comments.models import Comment
from likes.models import Like
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

def run():
    # Clear old data
    Post.objects.all().delete()
    User.objects.all().exclude(is_superuser=True).delete()
    print("Cleared old data.")

    # Create users
    user1 = User.objects.create_user(username='julius', email='julius@example.com', password='test1234')
    user2 = User.objects.create_user(username='banju', email='banju@example.com', password='test1234')
    user3 = User.objects.create_user(username='devgirl', email='devgirl@example.com', password='test1234')
    print("Users created.")

    # Create profiles (if not auto)
    Profile.objects.get_or_create(user=user1, bio="Just Julius", location="Kasarani")
    Profile.objects.get_or_create(user=user2, bio="Creative guy", location="Nairobi")
    Profile.objects.get_or_create(user=user3, bio="Python lover", location="Nyeri")

    # Follow relationships
    Follow.objects.get_or_create(follower=user1, following=user2)
    Follow.objects.get_or_create(follower=user1, following=user3)
    Follow.objects.get_or_create(follower=user2, following=user1)
    print("Follow data added.")

    # Sample images (dummy, make sure these exist in your media)
    dummy_image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

    # Create posts
    post1 = Post.objects.create(user=user1, caption="First post!", image=dummy_image)
    post2 = Post.objects.create(user=user2, caption="Sunny day 🌞", image=dummy_image)
    print("Posts created.")

    # Likes
    Like.objects.create(user=user2, post=post1)
    Like.objects.create(user=user3, post=post1)
    Like.objects.create(user=user1, post=post2)

    # Comments
    Comment.objects.create(user=user2, post=post1, body="Nice one!")
    Comment.objects.create(user=user3, post=post1, body="🔥🔥🔥")
    Comment.objects.create(user=user1, post=post2, body="Cool!")

    print("Dummy data added successfully.")
