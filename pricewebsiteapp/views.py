from django.shortcuts import render
from .scraper import scrape_hepsiburada_prices, scrape_mediamarkt_prices,scrape_teknosa_prices,scrape_trendyol_prices,find_cheapest_product
from .models import Product, Favourite
from decimal import Decimal
from .forms import CustomUserCreationForm, CustomPasswordChangeForm
import re
from fuzzywuzzy import fuzz
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import CreateView
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.


def view_mainpage(request):
    if request.method == 'GET':
        existing_products = Product.objects.all()
        results = []

        for product in existing_products:
            # Ürünü kullanıcıya göre işaretle
            if request.user.is_authenticated:
                # Kullanıcının favorileri
                user_favourites = request.user.favourite.values_list('product_id', flat=True)
                product.is_favourite = product.id in user_favourites
            else:
                product.is_favourite = False

            results.append(product)

        return render(request, 'base.html', {'all_products': results})


def favourites_page(request):
    favourites = Favourite.objects.filter(user=request.user)
    return render(request, "favourites.html", {'favourites':favourites})


def product_view(request):
    query = request.GET.get('q')
    existing_products = Product.objects.all()
    results = []

    for product in existing_products:
        score = fuzz.partial_ratio(query.lower(), product.name.lower())
        if score > 70:
            results.append(product)
    
    if results:
        return render(request, 'base.html', {'all_products':results})
    else:
        return render(request, 'base.html', {'message': 'Üzgünüz, böyle bir ürün bulamadık :( '})
        """     siteye veri eklemek istediğimde bu kısmı yorum satırından çıkaracağım.
        teknosa_cheapest = scrape_teknosa_prices(query)
        hepsiburada_cheapest = scrape_hepsiburada_prices(query)
        mediamarkt_cheapest = scrape_mediamarkt_prices(query)
        trendyol_cheapest = scrape_trendyol_prices(query)

        results = [hepsiburada_cheapest, trendyol_cheapest, mediamarkt_cheapest, teknosa_cheapest]
        cheapest = find_cheapest_product(results)
        saveproducts_todb(results)
        return render(request, 'base.html', {'cheapest':cheapest, 'all_products': results})
        """


def custom_logout(request):
    logout(request)
    return redirect('/')


def saveproducts_todb(products):

    for product in products:
        if product is None or product.price is None:
            print("Eksik değer atlanıyor.")
            continue

        clean_price = re.sub(r'[^\d,\.]', '', product.price)
        clean_price = clean_price.replace('.', '').replace(',', '.').replace('TL', '').replace('–', '').replace('-', '').replace('₺', '')
        print(f"Temiz fiyat kayıt: {clean_price}")
        
        try:
            decimalprice = Decimal(clean_price)
            print(type(decimalprice))
        except:
            print("dönüştürme hatası")

        Product.objects.update_or_create(
            name = product.name,
            defaults={
                'price': decimalprice,
                'image_url': product.image_url,
                'link': product.link,
                'site': product.site
            }
        )

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('pricewebsiteapp:home')
    template_name = "registration/changepassword.html"


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def add_to_favourites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not Favourite.objects.filter(user=request.user, product=product).exists():
        Favourite.objects.create(user=request.user, product=product)
        print(f"Added to favourites: {request.user.username}, Product: {product.name}")
    else:
        print(f"Already in favourites: {request.user.username}, Product: {product.name}")
    return redirect(request.META.get('HTTP_REFERER', 'home'))  # Fallback to home if REFERER is not present


@login_required
def remove_from_favourites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        favourite = Favourite.objects.get(user=request.user, product=product)
        print(f"Bulunan Favori: {favourite}")
        favourite.delete()
        print(f"Deleted favourite: {request.user.username}, Product: {product.name}")
    except Favourite.DoesNotExist:
        print(f"Favourite not found: user={request.user.username}, product={product.name}")
    return redirect(request.META.get('HTTP_REFERER', 'home'))  # Fallback to home if REFERER is not present

@login_required
def removefavourites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        favourite = Favourite.objects.get(user=request.user, product=product)
        favourite.delete()
        print(f"Deleted favourite: {request.user.username}, Product: {product.name}")
    except Favourite.DoesNotExist:
        print(f"Favourite not found: user={request.user.username}, product={product.name}")

    next_url = request.GET.get('next', reverse('pricewebsiteapp:favourites'))  # Varsayılan olarak favoriler sayfasına yönlendirir
    return HttpResponseRedirect(next_url)

