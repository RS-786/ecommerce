from django.urls import path
from . import views


urlpatterns = [
    path('',views.itemlist,name = "itemlist")
]