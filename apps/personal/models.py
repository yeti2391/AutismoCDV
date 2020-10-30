from django.db import models

# Create your models here.
class PersonalSkill(models.Model):
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.skill


class Personal(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to="personalThumbnails/")
    description = models.TextField(blank=True, null=True)
    skills = models.ForeignKey(PersonalSkill, on_delete=models.CASCADE, blank=True, null=True) #revisar si no tengo que cambiar el valor de on_delete
    mail = models.EmailField(max_length=100, blank=True, null=True)
    #agregar despues un field de recursos para descargar material nose si aca o en video mejor

    def __str__(self):
        return "%s %s" % (self.last_name, self.name)
