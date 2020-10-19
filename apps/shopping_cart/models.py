from django.conf import settings
from django.db import models
from apps.content.models import Course
# Create your models here.

class OrderItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.name

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    ref_code = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

#para seguimiento de las compras realizadas:
class Payment(models.Model):
    #revisar si en produccion combiene usar on_delete CASCADE ya que de borrarse
    #un payment se estaría borrando la orden tambien!!!!!
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    date_paid = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=100)

    def __str__(self):
        return self.stripe_charge_id
