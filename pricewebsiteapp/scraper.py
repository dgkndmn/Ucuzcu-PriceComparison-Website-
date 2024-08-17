from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from selenium.webdriver.chrome.options import Options
from .models import Product
from decimal import Decimal, InvalidOperation
import re
from fuzzywuzzy import fuzz


def scrape_trendyol_prices(query):
    driver = webdriver.Chrome('/Users/dogukan/chromedriver-mac-arm64/chromedriver')
    driver.get(f"https://trendyol.com/sr?q={query}")
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "p-card-wrppr.with-campaign-view")))

    products = driver.find_elements(By.CLASS_NAME, "p-card-wrppr.with-campaign-view")
    ty_data = []

    urunsayisi = 0
    aramasayisi = 0
    while (urunsayisi<1):
        for product in products:
            if urunsayisi >= 1:
                    break
            else:
                try:
                    productlink = product.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                    productimage = product.find_element(By.CLASS_NAME, "p-card-img").get_attribute('src')
                    productname = product.find_element(By.CLASS_NAME, "prdct-desc-cntnr-name").text
                    productprice = product.find_element(By.CLASS_NAME, "prc-box-dscntd").text
                except Exception:
                    aramasayisi += 1
                    if aramasayisi==20:
                        driver.quit()
                        return None
                    else:
                        continue


                if fuzz.partial_ratio(query.lower(), productname.lower()) > 10:
                        urunsayisi += 1
                        ty_data.append(
                        Product(
                            name=productname,
                            price=productprice,
                            image_url = productimage,
                            link = productlink,
                            site = "Trendyol"
                        )
                    )

                    
        driver.quit()
        ty_cheapest = find_cheapest_product(ty_data)
        return ty_cheapest


def find_cheapest_product(products):

    if not products:
        return None

    cheapest = None
    cheapest_price = Decimal('Infinity')  # Başlangıçta en yüksek değeri kullanıyoruz

    #fiyat temizleyelim
    for product in products:
        if product is None or product.price is None:
            continue
        else:
            price_str = str(product.price)
            clean_price = re.sub(r'[^\d,\.]', '', price_str)
            clean_price = clean_price.replace('.', '').replace(',', '.').replace('TL', '').replace('–', '').replace('-', '').replace('₺', '')

            print(f"Temiz fiyat kayıt: {clean_price}")
            
            try:
                decimalprice = Decimal(clean_price)
                print(type(decimalprice))
            except:
                print("dönüştürme hatası")

            if decimalprice < cheapest_price:
                cheapest_price = decimalprice
                cheapest = product
        
    print(f"Cheapest Product: {cheapest}")
    return cheapest

# en ucuzu myproducts = scrape_trendyol_prices('iphone 15')

def scrape_hepsiburada_prices(query):
    driver = webdriver.Chrome('/Users/dogukan/chromedriver-mac-arm64/chromedriver')
    try:
        driver.get(f"https://www.hepsiburada.com/ara?q={query}")
        WebDriverWait(driver, 50).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "[data-test-id='loader-false']")))

        hb_data = []
        urunsayisi = 0
        aramasayisi = 0

        while urunsayisi < 1 and aramasayisi < 20:
            products = driver.find_elements(By.CSS_SELECTOR, "[data-test-id='loader-false']")
            if not products:
                print("Ürünler bulunamadı.")
                aramasayisi += 1
                continue

            for product in products:
                print("Arama sayısı: ", aramasayisi)
                if urunsayisi >= 1:
                    break
                
                try:
                    productlink = product.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
                    productimage = product.find_element(By.XPATH, '//*[@id="i0"]/div/a/div[1]/div[1]/div[1]/div/picture/img').get_attribute('src')
                    productname = product.find_element(By.CSS_SELECTOR, "[data-test-id='product-card-name']").text
                    productprice = product.find_element(By.CSS_SELECTOR, "[data-test-id='price-current-price']").text
                    
                    # Eğer name veya price None ise
                    if not productname or not productprice:
                        print(f"Geçersiz ürün verisi, arama sayısı: {aramasayisi}")
                        continue

                except Exception as e:
                    aramasayisi += 1
                    print(f"Hata: {e}, arama sayısı: {aramasayisi}")
                    continue

                if fuzz.partial_ratio(query.lower(), productname.lower()) > 10:
                    urunsayisi += 1
                    hb_data.append(
                        Product(
                            name=productname,
                            price=productprice,
                            image_url=productimage,
                            link=productlink,
                            site="Hepsiburada"
                        )
                    )
                    break

            aramasayisi += 1

        if urunsayisi == 0:
            print("Arama sınırı aşıldı, uygun ürün bulunamadı.")
            return None
                    
    finally:    
        driver.quit()

    hb_cheapest = find_cheapest_product(hb_data)
    return hb_cheapest




def scrape_teknosa_prices(query):
    driver = webdriver.Chrome('/Users/dogukan/chromedriver-mac-arm64/chromedriver')
    driver.get(f"https://www.teknosa.com/arama/?s={query}")

    WebDriverWait(driver, 120).until(EC.visibility_of_all_elements_located((By.ID, "product-item")))

    products = driver.find_elements(By.ID, "product-item")
    tk_data = []

    urunsayisi = 0
    aramasayisi = 0
    while(urunsayisi<1):
        for product in products:
            if urunsayisi>=1:
                break
            else:
                try:
                    productlink = product.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    productimage = product.find_element(By.CLASS_NAME, "lazy.entered.loaded").get_attribute('srcset')
                    productname = product.find_element(By.CLASS_NAME, "prd-title.prd-title-style").text
                    productprice = product.find_element(By.CLASS_NAME, "prc.prc-last").text
                    print(f"Name: {productname}, Price: {productprice}, Image: {productimage}, Link: {productlink}")
                except Exception:
                    aramasayisi += 1
                    if aramasayisi==20:
                        driver.quit()
                        return None
                    else:
                        continue

                if fuzz.partial_ratio(query.lower(), productname.lower()) > 10:
                    urunsayisi += 1
                    tk_data.append(
                        Product(
                            name=productname,
                            price=productprice,
                            image_url = productimage,
                            link = productlink,
                            site = "Teknosa"
                        )
                    )


    driver.quit()
    tk_cheapest = find_cheapest_product(tk_data)
    return tk_cheapest
        
                    
def scrape_mediamarkt_prices(query):
    driver = webdriver.Chrome('/Users/dogukan/chromedriver-mac-arm64/chromedriver')
    driver.get(f"https://www.mediamarkt.com.tr/tr/search.html?query={query}")

    WebDriverWait(driver, 150).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "[data-test='mms-product-card']")))

    products = driver.find_elements(By.CSS_SELECTOR, "[data-test='mms-product-card']")
    mm_data = []

    urunsayisi = 0
    aramasayisi = 0
    while(urunsayisi<1):
        for product in products:
            if urunsayisi >= 1:
                break
            else:
                try:
                    productprice = product.find_element(By.CLASS_NAME, "sc-3f2da4f5-0.dievjx.sc-dd1a61d2-2.efAprc").text
                    productlink = product.find_element(By.CSS_SELECTOR, "[data-test='mms-product-list-item-link']").get_attribute('href')
                    productimage = product.find_element(By.CSS_SELECTOR, "[data-test='product-image'] img").get_attribute('src')
                    productname = product.find_element(By.CSS_SELECTOR, "[data-test='product-image'] img").get_attribute('alt')
                    print(f"Name: {productname}, Price: {productprice}, Image: {productimage}, Link: {productlink}")
                except Exception:
                    aramasayisi += 1
                    if aramasayisi==20:
                        driver.quit()
                        return None
                    else:
                        continue
                    

                if fuzz.partial_ratio(query.lower(), productname.lower()) > 70:
                    urunsayisi += 1
                    mm_data.append(
                        Product(
                            name=productname,
                            price=productprice,
                            image_url = productimage,
                            link = productlink,
                            site = "Mediamarkt"
                        )
                    )
                                 
    driver.quit()
    mm_cheapest = find_cheapest_product(mm_data)
    return mm_cheapest












