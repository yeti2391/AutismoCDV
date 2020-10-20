from django import template
from apps.shopping_cart.models import Order

#esto es propio de los templates de django:
register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, is_ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0
