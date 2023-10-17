from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

#10 тестов для данного REST API-интерфейса

#1 тест - добавляем информацию о питомце без фото (/api/create_pet_simple) с валидными данными:
def test_create_pet_simple_with_valid_data(name='Каспер', animal_type='Цвергшнауцер',
                                     age='2'):

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#2 тест - добавляем информацию о питомце без фото (/api/create_pet_simple) с невалидными данными (поле 'age' = str, а не number)
def test_create_pet_simple_with_invalid_data(name='Каспер', animal_type='Цвергшнауцер',
                                     age='four'):

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
# Фактический результат - найдена ошибка в api, поле 'age' должно принимать только number, а принимает string.

#3 тест - добавляем фото питомца (/api/pets/set_photo/{pet_id}) с валидными данными
def test_set_photo_with_valid_data(pet_photo='images/cat1.jpg'):

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового питомца без фото и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка
    pet_id = my_pets['pets'][0]['id']

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем фото
    status, result = pf.set_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200

#4 тест - запрос api ключа с невалидными данными (get/api/key)
def test_get_api_key_for_invalid_user(email="!@#", password="!@#"):

    #Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    #Сверяем полученные данные с нашими ожиданиями
    assert status == 403

#5 тест - Запрос списка питомцев с валидным фильтром filter=my_pets (get/api/pets)
def test_get_list_of_pets_with_valid_filter(filter='my_pets'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

#6 тест - Запрос списка питомцев с невалидным фильтром filter=pets (get/api/pets)
def test_get_list_of_pets_with_invalid_filter(filter='pets'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 400
    # Фактический результат - найдена ошибка в api, должна возвращаться 400 ошибка при невалидных данных, но сервер вернул 500

#7 тест - Добавление питомца (post/api/pets) с невалидными данными (текстовый файл вместо фото)
def test_add_new_pet_with_invalid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/1.txt'):

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    # Фактический результат - найдена ошибка в api, сервер принял текстовый файл вместо фото

#8 тест - Запрос списка питомцев без опционального параметра (filter)
def test_get_list_of_pets():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key)

    assert status == 200

#9 тест - Добавление питомца (post/api/pets) с невалидными данными (name, animal_type, age - пустые)
def test_add_new_pet_with_invalid_data_empty(name='', animal_type='',
                                     age='', pet_photo='images/cat1.jpg'):

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    # Фактический результат - найдена ошибка в api, сервер принимает пустые значения

#10 тест - удаление питомца с несуществующим pet_id
def test_unsuccessful_delete_self_pet():

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Указываем несуществующий id питомца и отправляем запрос на удаление
    pet_id = '!!'
    status, _ = pf.delete_pet(auth_key, pet_id)

    assert status == 400
    # Фактический результат - найдена ошибка в api, сервер возвращает 200 при невалидном pet_id