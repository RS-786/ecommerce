from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Item,OrderItem,Order,BillingAddress,Payment
from .forms import CheckoutForm
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import stripe
stripe.api_key = "sk_test_foRP96MM4gujWqr8Ggnwf06i00HZt23taZ"
P_key = "pk_test_tjoV1upnE5HnQ5PzoCAFbJoa00C2phujgW"


class IndexView(ListView):
    model = Item
    template_name = "website/index.html"

class ProductView(DetailView):
    model = Item
    template_name = "website/product.html"

def ViewCart(request,slug):
    order = Order.objects.get(slug = slug)
    items = order.items.all()
    context ={
        'object' : order,
        'items' : items
    }
    return render(request,"website/shopping-cart.html",context)


class CheckoutView(View):

    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context={
            'form':form
        }
        return render(self.request, "website/check-out.html",context)

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
                email = form.cleaned_data.get('email')

                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    city=city,
                    zip=zip,
                    phone=phone,
                    country=country,
                    email = email
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
            return redirect('payment')

        except ObjectDoesNotExist:
            return redirect('shoppingcart')

def Paymentfn(request):

    order = Order.objects.get(user=request.user, ordered=False)
    amount = int(order.get_total())
    name = order.user.username
    address = order.billing_address.street_address
    email = order.billing_address.email
    city = order.billing_address.city

    if request.method == 'GET':
        intent = stripe.PaymentIntent.create(
            amount= amount * 100,
            currency='inr',
            payment_method_types=['card'],
            description = "Test payment"
        )
        context = {
            'Publishable_key': P_key,
            'customer_email': email,
            'intent_id': intent.id,
            'customer_address' : address,
            'customer_name' : name,
            'city' : city
        }
        return render(request, "website/payment.html",context)

    if request.method == 'POST':
        intent_id = request.POST['intent_id']
        payment_method_id = request.POST['payment_method_id']
        stripe.api_key = "sk_test_foRP96MM4gujWqr8Ggnwf06i00HZt23taZ"
        stripe.PaymentIntent.modify(
            intent_id,
            payment_method = payment_method_id
        )
        stripe.PaymentIntent.confirm(intent_id)
        # create payment
        payment = Payment()
        payment.stripe_charge_id = intent_id
        payment.user = request.user
        payment.amount = amount
        payment.save()
        # assign payment to order
        order.ordered = True
        order.payment = payment
        order.save()

        messages.success(request, "Your order was placed successfully")
        return redirect("/")


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
        order = Order.objects.create(user=request.user,ordered_date=ordered_date,slug=request.user.username)
        order.items.add(order_item)     
        messages.info(request, "Item was added to your cart")

    return redirect("/")


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = get_object_or_404(OrderItem, item=item)
    order_item.delete()
    messages.info(request, "Item removed from cart!")

    return redirect("shoppingcart")