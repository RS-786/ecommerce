from django import template
from website.models import Order

register = template.Library()

@register.filter
def cart_item_count(user):
    qs = Order.objects.filter(user=user, ordered=False)
    return qs[0].items.count()
