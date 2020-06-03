from django.urls import path
from . import views


urlpatterns = [
    path('',views.IndexView.as_view(),name = "index"),
    path('categories',views.categories,name="categories"),
    path('product/<slug>',views.ProductView.as_view(),name="product"),
    path('shoppingcart/<slug>',views.ViewCart,name="shoppingcart"),
    path('checkout',views.CheckoutView.as_view(),name="checkout"),
    path('contact',views.contact,name="contact"),
    path('add-to-cart/<slug>',views.add_to_cart,name="add-to-cart"),
    path('remove-from-cart/<slug>',views.remove_from_cart,name ="remove-from-cart"),
    path('payment/<str:payment_option>',views.Paymentfn,name="payment"),
    path('search/<str:tag>',views.search,name="search")
]