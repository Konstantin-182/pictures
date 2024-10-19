import http.client  # Модуль для выполнения запросов HTTP
from duckduckgo_search import DDGS  # Класс для поиска изображений
import urllib.request  # Подмодуль для открытия URL
import urllib.error
import os  # Модуль для работы с операционной системой

class Image:
    def __init__(self, name_acter, num):
        self.name_acter = name_acter
        self.kolichestvo_image = 300
        self.dirictory = os.path.join(os.getcwd(), f'pictures/class{num}')
        if not os.path.exists(self.dirictory):
            os.makedirs(self.dirictory)  # Создание нового каталога

    def load_images(self, image_url, filename):
        try:
            urllib.request.urlretrieve(image_url, os.path.join(self.dirictory, filename))
            print('Скачано')
        except urllib.error.URLError:
            print('Ошибка')
        except TimeoutError:
            print('Долго')
        except http.client.RemoteDisconnected:
            print('Соединение закрылось')

    def search_images(self):
        results = DDGS().images(
            keywords=self.name_acter,  # Поисковый запрос
            region="wt-wt",  # Регион всемирный
            safesearch="off",
            size=None,  # Без разницы
            type_image=None,  # Тип изображения
            layout=None,  # Макет изображения
            license_image=None,  # Лицензия не ограничена
            max_results=self.kolichestvo_image  # Ограничение изображений до 300
        )
        url_list = [elem.get('image') for elem in results]  # Список URL адресов изображений
        name_acter_list = [f'{self.name_acter}{i}.jpg' for i in range(len(url_list))]  # Формат имени изображений
        return url_list, name_acter_list

if __name__ == '__main__':
    acters = ['Selena Gomez', 'Demi Lovato', 'Jean Reno', 'Robert De Niro', 'Tom Hanks', 'Tom Cruise']
    for num, actor in enumerate(acters, 1):
        img = Image(actor, num)  # Создание экземпляра класса
        url_list, name_acter_image = img.search_images()  # Получение списка URL и названий изображений
        for image_url, name_acter in zip(url_list, name_acter_image):
            img.load_images(image_url, name_acter)  # Скачивание изображений

import sys
print(sys.prefix)  # Показывает директорию виртуальной среды
print(__name__)  # Проверка имени модуля
