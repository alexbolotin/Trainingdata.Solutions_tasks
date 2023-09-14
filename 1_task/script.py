import os
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def create_directories_if_not_exist(brand, model):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    brand_folder = os.path.join(current_directory, brand)
    
    if not os.path.exists(brand_folder):
        os.makedirs(brand_folder)

    model_folder = os.path.join(brand_folder, model)
    i = 1
    while os.path.exists(model_folder):
        model_folder = os.path.join(brand_folder, f"{model} - {i}")
        i += 1
    
    os.makedirs(model_folder)
    return model_folder

def get_image_data(script_elements, number_of_image_per_car):
    images_list = []
    for script_element in script_elements:
        script_text = script_element.get_attribute('textContent')
        script_data = json.loads(script_text)
        if script_data.get('@type') == 'Product':
            images = script_data.get('image', [])
            for image in images:
                if image.get('@type') == 'ImageObject':
                    content_url = image.get('contentUrl')
                    width = image.get('width')
                    height = image.get('height')

                    if width is not None and height is not None:
                        area = width * height
                        images_list.append(
                            {'brand': script_data.get('brand'), 
                             'car_model': script_data.get('name'), 
                             'contentUrl': content_url, 
                             'area': area}
                        )
    # записываем ссылки - конкретная машина - ссылки на топ самых больших фотографий
    images_list.sort(key=lambda x: x['area'], reverse=True)
    
    # Если заданное количество изображений больше или равно количеству найденных изображений
    if number_of_image_per_car >= len(images_list):
        return images_list
    else:
        return images_list[:number_of_image_per_car]

def download_images(images_list, model_folder):
    # проходим по ссылкам на изображения
    for i, image_data in enumerate(images_list, start=1):
        content_url = image_data['contentUrl']
        
        # получаем ответ по ссылке на изображение
        response = requests.get(content_url)
        if response.status_code == 200:
            file_name = f'image_{i}.jpg'
            file_path = os.path.join(model_folder, file_name)
            
            # сохраняем изображение в папку
            with open(file_path, 'wb') as file:
                file.write(response.content)

def main():
    # Инициализация браузера
    driver = webdriver.Chrome()
    driver.get('https://auto.ru/')
    
    # кнопка согласия
    try:
        accept_button = driver.find_element(By.XPATH, '//a[text()="Я согласен. I accept"]')
        accept_button.click()
    except NoSuchElementException:
        pass
    
    # Извлекаем имя марки автомобиля
    elements = driver.find_elements(By.CLASS_NAME, 'IndexMarks__item')

    car_data = {}

    # сколько моделей машин взять:
    model_number = 10

    # сколько машин взять:
    car_number = 10

    # сколько изображений моделей машин взять:
    number_of_image_per_car = 5
    
    # записываем ссылки: марка машины - ссылка на страницу с машинами этой марки
    for element in elements[:model_number]:
        model_name = element.find_element(By.CLASS_NAME, 'IndexMarks__item-name').text
        model_link = element.find_element(By.CLASS_NAME, 'IndexMarks__item-name').find_element(By.XPATH, './ancestor::a').get_attribute('href')
        car_data[model_name] = model_link

    car_list = []
    
    # переходим по ссылкам на списки машин по марке
    for car, link in car_data.items():
        driver.get(link)
        listings = driver.find_elements(By.CLASS_NAME, 'ListingItemTitle__link')

        car_dict_list = []
        
        # записываем ссылки - список машин - ссылка на страницу с конкретной моделью машины
        for listing in listings[:car_number]:
            car_name = listing.text
            car_link = listing.get_attribute('href')
            car_dict = {'Car Name': car_name, 'Car Link': car_link}

            if car_name.strip() and car_link.strip():
                car_dict_list.append(car_dict)

        if car_dict_list:
            car_list.append({car: car_dict_list})
        
        # распаковываем список из словарей
        for car_dict in car_dict_list:
        
            # распаковываем словарь
            for key, value in car_dict.items():
                if key == 'Car Link':
                    driver.get(value)

                    script_elements = driver.find_elements(By.XPATH, '//script[@type="application/ld+json"]')
                    images_list = get_image_data(script_elements, number_of_image_per_car)
                    
                    # если что то пошло не так
                    if not images_list:
                        break

                    brand = images_list[0]['brand']
                    model = images_list[0]['car_model']
                    model_folder = create_directories_if_not_exist(brand, model)

                    download_images(images_list, model_folder)

    driver.quit()

if __name__ == "__main__":
    main()
