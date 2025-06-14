import requests
from bs4 import BeautifulSoup
import csv

url = "http://books.toscrape.com/catalogue/page-1.html"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.select("article.product_pod")

    with open("books_data.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["اسم الكتاب", "السعر", "رابط صورة الغلاف", "التقييم"])

        for book in books:
            # اسم الكتاب
            title = book.h3.a["title"]

            # السعر
            price = book.find("p", class_="price_color").text.strip()

            # رابط صورة الغلاف (نسبي)
            img_rel_url = book.find("img")["src"]
            img_url = "http://books.toscrape.com/" + img_rel_url.replace("../", "")

            # التقييم: يتم تمثيله بكلمة داخل class مثل "star-rating Three"
            rating_class = book.find("p", class_="star-rating")["class"]
            # التقييم هو الكلمة الثانية في قائمة الكلاسات
            rating_word = rating_class[1]

            # تحويل التقييم من كلمة إلى رقم (اختياري)
            ratings_map = {
                "One": 1,
                "Two": 2,
                "Three": 3,
                "Four": 4,
                "Five": 5
            }
            rating = ratings_map.get(rating_word, "غير معروف")

            writer.writerow([title, price, img_url, rating])
            print(f"✅ {title} - {price} - ⭐ {rating} - صورة: {img_url}")
else:
    print("❌ فشل في تحميل الصفحة")
