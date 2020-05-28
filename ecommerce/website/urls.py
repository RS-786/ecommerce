from django.urls import path
from . import views


urlpatterns = [
    path('',views.IndexView.as_view(),name = "index"),
    path('categories',views.categories,name="categories"),
    path('product/<slug>',views.ProductView.as_view(),name="product"),
    path('shoppingcart',views.shopping_cart,name="shoppingcart"),
    path('checkout',views.checkout,name="checkout"),
    path('contact',views.contact,name="contact"),
    path('add-to-cart/<slug>',views.add_to_cart,name="add-to-cart")
]