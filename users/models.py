from django.db import models
from login.models import *

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    poster = models.ForeignKey(User, related_name="posts_made", on_delete = models.CASCADE)
    receiver = models.ForeignKey(User, related_name="posts_on_wall", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)