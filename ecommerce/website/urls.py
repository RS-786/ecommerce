from django.urls import path
from . import views


urlpatterns = [
    path('',views.itemlist,name = "itemlist"),
    path('index',views.index,name = "index"),
    path('categories',views.categories,name="categories"),
    path('product-page',views.product_page,name="productpage"),
    path('shoppingcart',views.shopping_cart,name="shoppingcart"),
    path('checkout',views.checkout,name="checkout"),
    path('contact',views.contact,name="contact")
]