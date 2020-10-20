from django.db import models
from django.conf import settings
#1)voy a necesitar signals para crear este perfil de usuario con cada nuevo user
from django.db.models.signals import post_save
from apps.content.models import Course
# Create your models here.

class UserProfile(models.Model):
    #agregar opciones de me gusta
    #agregar despues una relacion con Product en store.models
    cursos = models.ManyToManyField(Course, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    #para ver que cosas efectivamente se compro:
    def cursos_list(self):
        return self.cursos.all()

    class Meta:
        verbose_name='Perfil de Usuario'
        verbose_name_plural = 'Perfiles de usuarios'


#1)signal para establecer relacion con cada nuevo usuario
def post_user_signup_receiver(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
#1)
post_save.connect(post_user_signup_receiver, sender=settings.AUTH_USER_MODEL)


#2)ahora vamos a hacer un if en el template para restringir acceso algo asi x ejemplo en content list:
# if course in request.user.userpprofile.cursos_list
# ahi muestre solucion

# else: algun mensaje q no tiene acceso y agregar alguna imagen de que no puede
