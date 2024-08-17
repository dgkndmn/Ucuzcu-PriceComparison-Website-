from django.contrib import admin
from django.urls import path
from . import views
from .views import product_view

app_name = 'pricewebsiteapp'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.view_mainpage, name="home"),
    path('search/', product_view, name="product_view")
]