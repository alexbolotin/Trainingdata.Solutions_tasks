import requests
from bs4 import BeautifulSoup # я делаю парсинг этой библиотекой библиотека

url = 'http://auto.ru' 

site = requests.post(url) # Делаем запрос 

soup = BeautifulSoup(site.text, "html.parser") # получаем ввесь Html страницы

content = soup.find('div').text # Получаем содержимое внутри всех тегов div на пример

print(soup) # Выводим Html