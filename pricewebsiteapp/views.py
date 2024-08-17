from django.shortcuts import render
from .scraper import scrape_hepsiburada_prices, scrape_mediamarkt_prices,scrape_teknosa_prices,scrape_trendyol_prices,find_cheapest_product
from .models import Product
from decimal import Decimal
import re

# Create your views here.

def view_mainpage(request):
    return render(request, 'base.html')


def product_view(request):
    query = request.GET.get('q')
    existing_products = Product.objects.filter(name__icontains=query)

    if existing_products.exists():
        print(f"Existing Products Sayısı: {existing_products.count()}")

        for product in existing_products:
            print(f"Product Name: {product.name} Price: {product.price} Image URL: {product.image_url} Link: {product.link} Site: {product.site}")

        print("bu kisima geldim")
        results = existing_products
        cheapest = find_cheapest_product(results)
        print(cheapest)
        return render(request, 'base.html', {'cheapest':cheapest, 'all_products': results})

    else:  
        hepsiburada_cheapest = scrape_hepsiburada_prices(query)
        mediamarkt_cheapest = scrape_mediamarkt_prices(query)
        trendyol_cheapest = scrape_trendyol_prices(query)
        teknosa_cheapest = scrape_teknosa_prices(query)
        
        
        results = [hepsiburada_cheapest, trendyol_cheapest, mediamarkt_cheapest, teknosa_cheapest]
        cheapest = find_cheapest_product(results)
        saveproducts_todb(results)
        return render(request, 'base.html', {'cheapest':cheapest, 'all_products': results})


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
       
    
    

