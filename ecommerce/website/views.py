from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Item,OrderItem,Order
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .templatetags.cart_template_tags import cart_item_count

class IndexView(ListView):
    model = Item
    template_name = "website/index.html"

class ProductView(DetailView):
    model = Item
    template_name = "website/product.html"

class ViewCart(ListView):
    model = OrderItem
    template_name = "website/shopping-cart.html"

def categories(request):
    return render(request,"website/categories.html")

def checkout(request):
    return render(request,"website/check-out.html")

def contact(request):
    return render(request,"website/contact.html")

def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug= slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,user = request.user,ordered = False)
    order_qs = Order.objects.filter(user = request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity updated")
        else:
            messages.info(request,"Item was added to your cart")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to your cart")
    return redirect("shoppingcart")


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = get_object_or_404(OrderItem, item=item)
    order_item.delete()
    messages.info(request, "Item removed from cart!")

    return redirect("shoppingcart")