from django.shortcuts import render
from .models import Item

def itemlist(request):
    context = {
        "items":Item.objects.all()
    }
    return render(request, "website/index.html",context)

def index(request):
    return render(request,"website/index.html")

def categories(request):
    return render(request,"website/categories.html")

def product_page(request):
    return render(request,"website/product-page.html")

def shopping_cart(request):
    return render(request,"website/shopping-cart.html")

def checkout(request):
    return render(request,"website/check-out.html")

def contact(request):
    return render(request,"website/contact.html")