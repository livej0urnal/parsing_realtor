import requests
from bs4 import BeautifulSoup
import csv
import json
import time
from openpyxl import load_workbook

# Сохраним страницу
# url = 'https://chicagorealtor.com/realtor-search/?sort&dir=SORT_DESC&rows_per_page=20050'
# headers = {
#     "Accept": "*/*",
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
# }
#
# req = requests.get(url, headers=headers)
# src = req.text
#
# with open("data/index.html", "w") as file:
#     file.write(src)


# Получаем все ссылки на страницы риэлторов
persons_url_list = []
with open("data/index.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
all_persons = soup.find_all("tr", class_='vcard')
count = 1
fn = 'example.xlsx'
book = load_workbook(fn)
sheet = book.active
#Базовые колонки
sheet['A1'] = 'First Name'
sheet['B1'] = 'Last Name'
sheet['C1'] = 'Profile URL'
sheet['D1'] = 'Company'
sheet['E1'] = 'Zip'
sheet['F1'] = 'Email'
sheet['G1'] = 'City'
#цикл получения информации
for item in all_persons:
    person_url = item.find(class_="user_login").find("a").get("href")
    person_first_name = item.find(class_="first_name").text.strip()
    person_last_name = item.find(class_="last_name").text.strip()
    person_company = item.find(class_="company_name").text
    person_city = item.find(class_="city").text
    person_zip = item.find(class_="zip").text.strip()
    count += 1
    try:
        person_email = item.find(class_="user_email").find("a").get("href")
        person_email = person_email.replace("mailto:", '')
    except:
        person_email = " "
    print(person_url + ' ' + person_first_name + ' ' + person_email )
    print(count)
    #формируем массив данных
    data = (person_first_name, person_last_name, person_url, person_company, person_zip, person_email, person_city)
    persons_url_list.append(data)
#в цикле записываем data в таблицу
for row in persons_url_list:
    sheet.append(row)
book.save(fn)
book.close()
