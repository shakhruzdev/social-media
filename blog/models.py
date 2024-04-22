from django.db import models

from authentication.models import MyUser


class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='post/', null=True, blank=True)
    is_published = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    like_count = models.ManyToManyField(MyUser, related_name='post_likes', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def number_of_likes(self):
        return self.like_count.count()

    def __str__(self):
        return f'{self.author.user.username}'


class Comment(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.CharField(max_length=150)
    is_visible = models.BooleanField(default=True)
    comments_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class Follow(models.Model):
    follower = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='follower_user')
    following = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='following_user')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
