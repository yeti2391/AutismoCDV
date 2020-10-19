from django.conf import settings
from django.db import models
#se importa la siguiente señal para mejorar el tema de slugs en course y video
#tambien es necesario el pre_save:
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
#hasta aca señales
from django.shortcuts import reverse


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to="courseThumbnails/")
    publish_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    description = models.TextField()
    price = models.FloatField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("content_app:course-detail", kwargs={"slug":self.slug})



class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    videofile = models.FileField(upload_to='courseVideos', null=True, verbose_name="videos de curso")
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    #quizas agragar un campo tipo para descargar recursos que acompañen el video
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("content_app:video-detail", kwargs={
            "video_slug":self.slug,
            "slug":self.course.slug
        })


def pre_save_course(sender,instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

def pre_save_video(sender,instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_course, sender=Course)
pre_save.connect(pre_save_video, sender=Video)
