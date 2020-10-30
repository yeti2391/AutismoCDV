from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest, OrdersCaptureRequest
from apps.shopping_cart.models import Order
from user.models import UserProfile
from .models import Compra, Payment
#from apps.content.models import Product, Course

import sys, json

#validacion por parte del servidor. viene despues de todo lo sacado en la documentacion de abajo
#si alguien realiza cambios en la transaccion de precios q la misma no se lleve a cabo
def pago(request):
    #order = Order.objects.all()
    #Experimento para obtener el valor total de la orden:

    order = get_object_or_404(Order, user=request.user)
    payment = Payment()
    payment.order = order
    payment.total_amount = float(order.get_total())
    payment.save()
    print('payment:' + str(payment.total_amount))
    #hasta aca experimento


    #esta es la order_id que va a utilizar abajo en capture transaccion y la funcion onApprove
    data = json.loads(request.body)
    order_id = data['orderID']
    print('order_id: ' + order_id)

    detalle = GetOrder().get_order(order_id) #aca esta toda la info de la transaccion
    #(se pueden ver todos los valores en la doc de PayPal, en Orders, Show order details)
    #y para capturar un valor de esa orden por ejemplo el precio:
    detalle_precio = float(detalle.result.purchase_units[0].amount.value)
    print('detalle_precio: ' + str(detalle_precio))

    #para la validacion: (adaptar correctamente a mis modelos)
    #fijarse si aca no es donde tengo que pasar el curso comprado al perfil de usuario
    # linea original: if detalle_precio == curso.price:
    if detalle_precio == payment.total_amount:
        trx = CaptureOrder().capture_order(order_id, debug=True)
        print('transaccion: ' + trx.result.id)
        #  a continuacion modelo Compra = documentacion Paypal
        pedido = Compra(
            id= trx.result.id,
            estado= trx.result.status,
            codigo_estado= trx.status_code,
            #producto= Producto.objects.get(pk=1),    ESTA ES LA LINEA ORIGIANL DEL CODIGO QUE GUARDA 1 PRODUCTO A 1 USUARIO

            #cursos= [Order.objects.filter(pk=order_id)],  DE ACA A LA LINEA 60 SON INTENTOS DE HACER EL GUARDADO SIN EXITO NO LAS BORRE PARA NO ANDAR MODIFICANDO EL NUMERO DE LINEA CON EL ARCHIVO DE ERROR

            #cursos = [item.course for item in order.items.all(),
            #users = User.objects.filter(email__in=emails)
            #instance = Setupuser.objects.create(organization=org)

            #for user in users:
            #    instance.emails_for_help.add(user)
            #for curso in cursos:
            #    request.user.UserProfile.cursos.add(curso)
            total_de_la_compra = trx.result.purchase_units[0].payments.captures[0].amount.value,
            nombre_cliente= trx.result.payer.name.given_name,
            apellido_cliente= trx.result.payer.name.surname,
            correo_cliente= trx.result.payer.email_address,
            direccion_cliente= trx.result.purchase_units[0].shipping.address.address_line_1)
        pedido.save() #guardamos en base de datos la info de la Transaccion
        #la funcion json en el html esta pidiendo una respuesta por lo q se le pasa esta variable data:
        pedido.cursos.set(Order.objects.filter(id=order_id))   #ESTO ES LO QUE HAY QUE MODIFICAR PARA QUE GUARDE LOS CURSOS EN COMPRA
        print(pedido.cursos)
        data = {
            "id": f"{trx.result.id}",
            "nombre_cliente": f"{trx.result.payer.name.given_name}",
            "mensaje": "Ahora ya puedes acceder al contenido! =D"
        }
        return JsonResponse(data)
    else:
        data = {
            "mensaje": "Error =( "
        }
        return JsonResponse(data)


#sacado de la documentacion de paypal
class PayPalClient:
    def __init__(self):
        self.client_id = "AbyTJKwLUxHVds6t59uuHQ72ANO9vIDp1LnRV-2dppHPglV_SxhqyVZh09IwnBDPaYW1urYxPNfgbPbm"
        self.client_secret = "EMEfyVXgJyorQGNCC-R8a3x2W5X69HVhbsq1rokcpCua2amqtdFEdoK_Ax7OzNGenB-xP3SEHVsM2oYU"

        """Set up and return PayPal Python SDK environment with PayPal access credentials.
           This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance with environment that has access
            credentials context. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key,value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
                        self.object_to_json(value) if not self.is_primittive(value) else\
                         value
        return result
    def array_to_json_array(self, json_array):
        result =[]
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if  not self.is_primittive(item) \
                              else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)



# sacado de la documentacion de paypal: https://developer.paypal.com/docs/checkout/reference/server-integration/get-transaction/#on-the-server
# es para obtener los detalles de la transaccion
class GetOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """You can use this function to retrieve an order by passing order ID as an argument"""
  def get_order(self, order_id):
    """Method to get order"""
    request = OrdersGetRequest(order_id)
    #3. Call PayPal to get the transaction
    response = self.client.execute(request)
    return response
    #4. Save the transaction in your database. Implement logic to save transaction to your database for future reference.
    """print 'Status Code: ', response.status_code
    print 'Status: ', response.result.status
    print 'Order ID: ', response.result.id
    print 'Intent: ', response.result.intent
    print 'Links:'
    for link in response.result.links:
      print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
    print 'Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
                       response.result.purchase_units[0].amount.value)

This driver function invokes the get_order function with
   order ID to retrieve sample order details.
if __name__ == '__main__':
  GetOrder().get_order('REPLACE-WITH-VALID-ORDER-ID')"""

#Hasta aca https://developer.paypal.com/docs/checkout/reference/server-integration/get-transaction/#on-the-server


#docu: https://developer.paypal.com/docs/checkout/reference/server-integration/capture-transaction/#on-the-server
#capture transaction
class CaptureOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """this sample function performs payment capture on the order.
  Approved order ID should be passed as an argument to this function"""

  def capture_order(self, order_id, debug=False):
    """Method to capture order using order_id"""
    request = OrdersCaptureRequest(order_id)
    #3. Call PayPal to capture an order
    response = self.client.execute(request)
    #4. Save the capture ID to your database. Implement logic to save capture to your database for future reference.
    if debug:
      print ('Status Code: ', response.status_code)
      print ('Status: ', response.result.status)
      print ('Order ID: ', response.result.id)
      print ('Links: ')
      for link in response.result.links:
        print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
      print ('Capture Ids: ')
      for purchase_unit in response.result.purchase_units:
        for capture in purchase_unit.payments.captures:
          print ('\t', capture.id)
      print ("Buyer:")
      """print "\tEmail Address: {}\n\tName: {}\n\tPhone Number: {}".format(response.result.payer.email_address,
        response.result.payer.name.given_name + " " + response.result.payer.name.surname,
        response.result.payer.phone.phone_number.national_number)"""
    return response


"""This driver function invokes the capture order function.
Replace Order ID value with the approved order ID. """
""" lo comento porque estoy usando una funcion para los mismo hecha arriba (pago)
if __name__ == "__main__":
  order_id = 'REPLACE-WITH-APPORVED-ORDER-ID'
  CaptureOrder().capture_order(order_id, debug=True)"""
#esto de arriba es el onapprove transaction en el html... ese order_id es la señal q necesito para guardar en el perfil


  #hasta aca https://developer.paypal.com/docs/checkout/reference/server-integration/capture-transaction/#on-the-server
