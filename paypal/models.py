from django.db import models
from apps.shopping_cart.models import Order

# Create your models here.


#esto seria para mis modelos cursos, y productos
"""class Producto(models.Model):
    producto = models.CharField(max_length=100, null= False)
    precio = models.DecimalField(max_digits=5 ,decimal_places= 2)

    def __str__(self):
        return self.producto
"""

#
class Compra(models.Model):
    id = models.CharField(primary_key= True, max_length=100)
    estado = models.CharField(max_length=100)
    codigo_estado = models.CharField(max_length=100)
    #producto = models.ForeignKey(to=Producto, on_delete= models.SET_NULL, null = True)
    total_de_la_compra = models.DecimalField(max_digits=5 ,decimal_places= 2)
    nombre_cliente = models.CharField(max_length=100)
    apellido_cliente = models.CharField(max_length=100)
    correo_cliente = models.EmailField(max_length=100)
    direccion_cliente = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Facturacion'
        verbose_name_plural= 'Facturaciones'

    def __str__(self):
        return str(self.nombre_cliente)



class Payment(models.Model):
    #revisar si en produccion combiene usar on_delete CASCADE ya que de borrarse
    #un payment se estaría borrando la orden tambien!!!!!
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order.user)

"""
codigo original
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
