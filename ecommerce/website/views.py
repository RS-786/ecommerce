from django.shortcuts import render,get_object_or_404,redirect
from .models import Item,OrderItem,Order
from django.views.generic import ListView, DetailView
from django.utils import timezone

class IndexView(ListView):
    model = Item
    template_name = "website/index.html"

class ProductView(DetailView):
    model = Item
    template_name = "website/product.html"

def categories(request):
    return render(request,"website/categories.html")


def shopping_cart(request):
    return render(request,"website/shopping-cart.html")

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
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("product",slug=slug)