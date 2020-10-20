from django.shortcuts import render
from django.core.mail import EmailMessage
from .forms import ContactForm
from django.views import View
from django.conf import settings



def contact(request):
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        #contact_form = ContactForm(data=request.POST)
        if form.is_valid():
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            file = request.FILES
            content = request.POST.get('content', '')

            # Creamos el correo
            email = EmailMessage(
                "Autismo Camino de Vida: Nuevo mensaje de contacto",
                "De {} <{}>\n\nEscribió:\n\n{}".format(name, email, content, file),
                "no-contestar@inbox.mailtrap.io",
                ["autismocdv@gmail.com"],
                reply_to=[email]
            )
            uploaded_file = request.FILES['file'] # file is the name value which you have provided in form for file field
            email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)

            #email.attach(file.name, file.read(), file.content_type)
            # Lo enviamos y redireccionamos
            try:
                email.send()
                # Todo ha ido bien, redireccionamos a OK
                return render(request, 'contacto/correo_enviado.html')
            except:
                # Algo no ha ido bien, redireccionamos a FAIL
                return render(request, 'contacto/correo_no_enviado.html')

    return render(request, "contacto/contact.html",{'form':form})
