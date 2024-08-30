from django.contrib import admin
from django.urls import path
from . import views
from .views import product_view

app_name = 'pricewebsiteapp'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.view_mainpage, name="home"),
    path('search/', product_view, name="product_view"),
    path("signup/", views.SignUpView.as_view(), name='signup'),
    path("changepassword/", views.CustomPasswordChangeView.as_view(), name="changepassword"),
    path("favourites/", views.favourites_page, name="favourites"),
    path("add-to-favourites/<int:product_id>/", views.add_to_favourites, name="add_to_favourites"),
    path("remove_from_favourites/<int:product_id>/", views.remove_from_favourites, name="remove_from_favourites"),
    path("removefavourites/<int:product_id>/", views.removefavourites, name="removefavourites")
]