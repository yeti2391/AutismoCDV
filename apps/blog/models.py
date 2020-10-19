from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    thumbnail = models.ImageField()
    publish_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug =models.SlugField(unique=True)

    class Meta:
        ordering = ["-publish_date"]


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_app:detail', kwargs={
            'slug': self.slug
        })


    def get_like_url(self):
        return reverse('blog_app:like', kwargs={
            'slug': self.slug
        })

    @property
    def comments(self):
        return self.comment_set.all()

    @property
    def get_comment_count(self):
        return self.comment_set.all().count()

    @property
    def get_view_count(self):
        return self.postview_set.all().count()

    @property
    def get_like_count(self):
        return self.like_set.all().count()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Vista de Post"
        verbose_name_plural = "Vistas de Posts"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Me gusta"
        verbose_name_plural = "Me gusta"
