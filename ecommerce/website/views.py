from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Item,OrderItem,Order,BillingAddress
from .forms import CheckoutForm
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
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

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form' : form
        }
        return render(self.request, "website/check-out.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user = self.request.user,ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                city = form.cleaned_data.get('city')
                zip = form.cleaned_data.get('zip')
                phone = form.cleaned_data.get('phone')
                country = form.cleaned_data.get('country')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    city=city,
                    zip=zip,
                    phone=phone,
                    country=country
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
            return redirect('/')

        except ObjectDoesNotExist:
            return redirect('shoppingcart')



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