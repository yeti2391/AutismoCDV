from django.shortcuts import render
from django.core.mail import EmailMessage
from .forms import ContactForm


def inicio(request):
    
    contact_form = ContactForm()

    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            content = request.POST.get('content', '')

            # Creamos el correo
            email = EmailMessage(
                "ONG prueba: Nuevo mensaje de contacto",
                "De {} <{}>\n\nEscribió:\n\n{}".format(name, email, content),
                "no-contestar@inbox.mailtrap.io",
                ["ongautismouy@gmail.com"],
                reply_to=[email]
            )

            # Lo enviamos y redireccionamos
            try:
                email.send()
                # Todo ha ido bien, redireccionamos a OK
                return render(request, 'contacto/correo_enviado.html')
            except:
                # Algo no ha ido bien, redireccionamos a FAIL
                return render(request, 'contacto/correo_no_enviado.html')

    return render(request, "core/home.html",{'form':contact_form})
