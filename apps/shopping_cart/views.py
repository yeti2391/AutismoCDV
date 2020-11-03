from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from apps.content.models import Course
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

# Create your views here.
@login_required
def add_to_cart(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    order_item, created= OrderItem.objects.get_or_create(course=course) #esto hace coincidir course de estaa func. con el course de OrderItem
    #order, created = Order.objects.get_or_create(user=request.user) se modifica esta linea por la siguiente:
    order, created = Order.objects.get_or_create(user=request.user, is_ordered=False)
    order.items.add(order_item)
    order.save()
    #agregar mensajes para visualizar la accion
    #messages.info(request, "Se agrego correctamente a su carrito de compras.")
    #return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
@login_required
def remove_from_cart(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    order_item= get_object_or_404(OrderItem, course=course)
    #order = get_object_or_404(Order, user=request.user) se cambia por:
    order = Order.objects.get(user=request.user, is_ordered=False)
    order.items.remove(order_item)
    order.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@login_required
def order_view(request):
    #order = get_object_or_404(Order, user=request.user)
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        context = {
            'order':order_qs[0]
        }
        return render(request, "shopping_cart/order_summary.html", context)
    return Http404


#para tomar la orden de compra:

"""
#agregados para pagar por stripe adaptar:
#esto deberia ir arriba del todo:
import random
import string
import stripe
from django.conf import settings
from django.shortcuts import redirect

stripe.api_key=settings.STRIPE_SECRET_KEY

#arriba tmb creo la siguiente funcion:
def create_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15)) #lista de letras y numeros random de largo 15

@login_required
def checkout(request):
    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order:order_qs[0]
    else:
        return Http404
    if request.method == "POST":
        #complete the order (ref code and set ordered to true)
        order.ref_code = create_ref_code()

        #create a stripe charge
        token = request.POST.get('strupeToken')
        charge = stripe.Charge.create(
            amount=int(order.get_total() * 100), #esta en cents x eso se multiplica x 100
            currency="usd",
            source="token",
            description="Charge for {request.user.username}"
        )



        #create our payment object and link to the order

        payment = Payment()
        payment.order = order
        payment.stripe_charge_id=charge.id #este id es devuelto por stripe al realizar una compra
        payment.total_amount = order.get_total()
        payment.save()

        #add the book to de user bool list
        books = [item.book for item in order.items.all()]
        for book in books:
            request.user.userlibrary.books.add(book)

        order.is_ordered =True #estas dos lineas son importante guardan la orden para dejar asentado la compra
        order.save()

        #redirect to user profile
        return redirect("/accounts/profile/")

    context = {
        'order':order
    }
    return render(request, "checkout.html", context)
"""
"""
modelos originales:

class UserLibrary(models.Model):
    books = models.ManyToManyField('Book') #se pone entre '' por esta referenciado abajo de esta class
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    #para ver que cosas efectivamente se compro:
    def book_list(self):
        return self.books.all()

    class Meta:
        verbose_name='Perfil de Usuario'
        verbose_name_plural = 'Perfiles de usuarios'


class Author(models.Model):
    first_name
    last_name
    slug

    def __str__
        return

class Book(models):
    authors = ManyToManyField
    head_title
    publications_date
    isbn
    slug
    civer
    price

class Chapter( mode)
     book = ForeignKey
     chapter_number
     title

----------------
models shopcart:


class OrderItem(models.Model):
    book = models.ForeignKey(book, on_delete=models.CASCADE)


class Order(models):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_ordered = models.Boolesa
    items = models.ManyToManyField (OrderItem)
    ref_code = models.CharField

class Payment():
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_amount
    date_paid
    stripe_charge_id


"""
