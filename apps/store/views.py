from django.shortcuts import render
from django.http import JsonResponse
#decorador que restringe a donde podes entrar solicitandoe star logiado
#el decorador se pone arriba de la vista: login_required(login_url='accounts_app:login')
from django.contrib.auth.decorators import login_required
from .models import *
import json
import datetime

# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        #esta excepcion es necesaria para poder ver el carrito no estando logueado
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        #y la siguiente linea permite agregar al carrito no estando logueado
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

login_required(login_url='accounts_app:login')
def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        #esta excepcion es necesaria para poder ver el carrito no estando logueado
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        #para actualizar items en carrito igual q store:
        cartItems = order['get_cart_items']


    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

login_required(login_url='accounts_app:login')
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        #esta excepcion es necesaria para poder ver el carrito no estando logueado
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']


    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

login_required(login_url='accounts_app:login')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ', action)
    print('ProductId: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

#se agrega esta importacion para solucionar que al estar AnonymousUser
#no se generaba el csrftoken correspondiente
#esto es una solucion temporal que deberia corregirse en el video 5
#from django.views.decorators.csrf import csrf_exempt
#tmb se agrega:
#@csrf_exempt
login_required(login_url='accounts_app:login')
def processOrder(request):
    #Solo para probar que se este dando correctamente la orden de pago (comentar de print hasta render para la prueba)
    #print('Data: ', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    #configuracion de orden para usuario atentificado y anonimo
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(str(data['form']['total'].strip().replace(',','.')))
        # Me da error que no se puede convertir una string en float la linea d abajo por eso modifique a la de arriba
        #total = float(data['form']['total'])
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
