from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from apps.content.models import Course
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

# Create your views here.
@login_required
def add_to_cart(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    order_item, created= OrderItem.objects.get_or_create(course=course) #esto hace coincidir course de estaa func. con el course de OrderItem
    order, created = Order.objects.get_or_create(user=request.user)
    order.items.add(order_item)
    order.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
@login_required
def remove_from_cart(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    order_item= get_object_or_404(OrderItem, course=course)
    order = get_object_or_404(Order, user=request.user)
    order.items.remove(order_item)
    order.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@login_required
def order_view(request):
    order = get_object_or_404(Order, user=request.user)
    context = {
        'order':order
    }
    return render(request, "shopping_cart/order_summary.html", context)



#para tomar la orden de compra:
"""@login_required
def processOrder(request):
    #Solo para probar que se este dando correctamente la orden de pago (comentar de print hasta render para la prueba)
    print('Data: ', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    #configuracion de orden para usuario atentificado y anonimo
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        #esto hace un chequeo de precio para verificar que desde el frontend no haya una modificacion en el precio:
        total = float(str(data['form']['total'].strip().replace(',','.')))

        order.transaction_id = transaction_id

        #se agrega lo siguiente para chequear que lo que se procesa desde el frontend coincida
        # con los datos del backend para evitar manipulacion de precio por parte de usuarios:
        if total == order.get_cart_total:
            order.complete = True
        order.save()

        #se configura el envio:
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in...')
    return JsonResponse('Pago completado', safe=False)
"""
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
    order = get_object_or_404(Order, user=request.user)
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
        books = item.book for item in order.items.all()
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
