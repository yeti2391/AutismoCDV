from django.conf import settings
from django.db import models

# Create your models here.

#class OrderItem(models.Model):


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    #items
    ref_code = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
