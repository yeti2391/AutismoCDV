from django.conf import settings
from django.db.models import Sum
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
    #ref_code = models.CharField(max_length=50)
    #agregar para store:
    #billing_address = models.ForeignKey(Address, related_name='billing_address', blank=True, null=True, on_delete=models.SET_NULL)
    #shipping_address = models.ForeignKey(Address, related_name='shipping_address', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username

    #para obtener el total de compras (se usa en order_summary.html):
    def get_total(self):
        return self.items.all().aggregate(order_total=Sum('course__price'))['order_total']


#para agregar los productos de la store:
"""
class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity =models.PositiveIntegerField(default=1)

class Address(models.Model):
    ADDRESS_CHOICES = (
        ('B', 'Billing'),
        ('S', 'Shipping'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    address_type = models.CharField(max_length=1, choices= ADDRESS_CHOICES)
    default= models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line_1}, {self.address_line_2}, {self.city}, {self.zip_code}"
    class Meta:
        verbose_name_plural='Addresses'
"""
"""
#lo dejo todo comentado payment porq al usar paypal en lugar de stripe lo hace auto
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
"""
