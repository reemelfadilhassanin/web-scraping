import requests
from bs4 import BeautifulSoup
import csv

# روابط الصفحتين
urls = [
    'http://books.toscrape.com/catalogue/page-1.html',
    'http://books.toscrape.com/catalogue/page-2.html'
]

books_data = []

for url in urls:
    print(f"🔍 تحميل البيانات من: {url}")
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')

        for book in books:
            # اسم الكتاب
            title = book.h3.a['title']

            # السعر
            price = book.find('p', class_='price_color').text

            # رابط صفحة الكتاب الداخلية
            book_link = book.h3.a['href']
            book_page_url = "http://books.toscrape.com/catalogue/" + book_link.replace('../../../', '')

            # تحميل الصفحة الداخلية للحصول على عدد المراجعات
            book_response = requests.get(book_page_url, headers={"User-Agent": "Mozilla/5.0"})
            book_soup = BeautifulSoup(book_response.text, 'html.parser')

            # استخراج عدد المراجعات من الجدول
            table = book_soup.find('table', class_='table table-striped')
            num_reviews = table.find_all('tr')[-1].find('td').text  # آخر صف هو عدد المراجعات

            # حفظ البيانات (بدون الصورة)
            books_data.append([title, price, num_reviews])

    else:
        print(f"⚠️ فشل في تحميل {url}")

# حفظ البيانات في ملف CSV
with open('books_with_reviews.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Number of Reviews'])
    writer.writerows(books_data)

print("✅ تم حفظ البيانات في ملف books_with_reviews.csv")
