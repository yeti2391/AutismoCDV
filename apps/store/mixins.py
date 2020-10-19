from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Product

class ProductPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs["slug"])
        #Necesito cambiar sucription y pricing_tier x una variable o señal de compra para el usuario
        subscription = request.user.subscription
        pricing_tier = subscription.pricing
        if not pricing_tier in course.pricing_tiers.all():
            messages.info(request, "No tienes acceso a este curso")
            return redirect("content:course-list")
        return super().dispatch(request, *args, **kwargs)
