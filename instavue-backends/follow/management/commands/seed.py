# follow/management/commands/seed.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from posts.models import Post
from likes.models import Like
from comments.models import Comment
from follow.models import Follow
from profiles.models import Profile
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import random, os

fake = Faker()
User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with users, profiles, posts, comments, likes, and follows'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("⚠️  Clearing non-superuser data..."))
        User.objects.exclude(is_superuser=True).delete()
        Profile.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()
        Like.objects.all().delete()
        Follow.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("✅ Old data cleared."))

        profile_pics_path = 'media/sample_profiles'
        profile_pics = [os.path.join(profile_pics_path, img) for img in os.listdir(profile_pics_path) if img.endswith(('.jpg', '.jpeg', '.png'))]

        # 🔐 Create special users
        special_users_data = [
            {'username': 'julius', 'email': 'julius@example.com'},
            {'username': 'banju', 'email': 'banju@example.com'},
        ]
        users = []

        for data in special_users_data:
            user, _ = User.objects.get_or_create(username=data['username'], defaults={
                'email': data['email'],
                'password': 'test1234'
            })
            img_path = random.choice(profile_pics)
            with open(img_path, 'rb') as f:
                Profile.objects.get_or_create(user=user, defaults={
                    'bio': fake.sentence(),
                    'location': fake.city(),
                    'profile_picture': File(f),
                })
            users.append(user)

        self.stdout.write(self.style.SUCCESS("👤 Special users created: julius, banju"))

        # 🧪 Create random users
        for _ in range(50):
            username = fake.user_name()
            email = fake.email()
            user = User.objects.create_user(username=username, email=email, password="test1234")
            img_path = random.choice(profile_pics)
            with open(img_path, 'rb') as f:
                Profile.objects.get_or_create(user=user, defaults={
                    'bio': fake.sentence(),
                    'location': fake.city(),
                    'profile_picture': File(f),
                })
            users.append(user)

        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(users)} users and profiles."))

        # 📝 Create posts
        posts = []
        for user in users:
            for _ in range(random.randint(1, 3)):
                post = Post.objects.create(
                    user=user,
                    caption=fake.sentence(),
                    image=SimpleUploadedFile("img.jpg", b"fake image", content_type="image/jpeg")
                )
                posts.append(post)

        self.stdout.write(self.style.SUCCESS(f"📝 Created {len(posts)} posts."))

        # ❤️ Likes
        for post in posts:
            likers = random.sample(users, random.randint(1, 10))
            for liker in likers:
                if liker != post.user:
                    Like.objects.get_or_create(user=liker, post=post)
        self.stdout.write(self.style.SUCCESS("❤️ Likes added."))

        # 💬 Comments
        for post in posts:
            for _ in range(random.randint(0, 5)):
                commenter = random.choice(users)
                Comment.objects.create(user=commenter, post=post, body=fake.text(max_nb_chars=50))
        self.stdout.write(self.style.SUCCESS("💬 Comments added."))

        # 👥 Follows
        for user in users:
            followees = random.sample(users, random.randint(3, 10))
            for followee in followees:
                if user != followee:
                    Follow.objects.get_or_create(follower=user, following=followee)
        self.stdout.write(self.style.SUCCESS("👥 Follow relationships added."))

        self.stdout.write(self.style.SUCCESS("🎉 Seeding complete!"))
