from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from apps.content.models import Course
from .models import Order, OrderItem

# Create your views here.
def add_to_cart(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    order_item, created= OrderItem.objects.get_or_create(course=course) #esto hace coincidir course de estaa func. con el course de OrderItem
    order, created = Order.objects.get_or_create(user=request.user)
    order.items.add(order_item)
    order.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def remove_from_cart(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    order_item= get_object_or_404(OrderItem, course=course)
    order = get_object_or_404(Order, user=request.user)
    order.items.remove(order_item)
    order.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
