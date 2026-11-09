import vk_api
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
access_token = os.getenv('VK_TOKEN')
user_id = os.getenv('ID')
app_id = os.getenv('APP_ID')
token = os.getenv('TOKEN')


def api_user(access_token):
    """Получаем api пользователя"""
    user=vk_api.VkApi(token=access_token)
    api = user.get_api()
    return api

api = api_user(access_token)
city = 'Санкт-Петербург'
#
#
def get_city_id(city,api):
    """Получаем ID города"""
    cities = api.database.getCities(
        country_id=1,      # 1 — Россия
        q=city,            # Поиск по названию
        count=1            # Нам нужен только первый результат
    )
    # Извлекаем ID
    city_id = cities['items'][0]['id']
    return city_id


city_id = get_city_id(city,api)
print(city_id)


def bdate_to_age(bdate: str) -> int | None:
    """Возвращает возраст числом или None, если год скрыт."""
    if not bdate:
        return None

    parts = bdate.split('.')
    if len(parts) != 3:          # "DD.MM" — год скрыт, возраст неизвестен
        return None

    day, month, year = map(int, parts)
    today = datetime.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age

def get_user_info(api,user_id):
    """Получаем информацию о пользователе"""
    user = api.users.get(user_ids=user_id,fields='city,sex,bdate')[0]
    user_info = {'id': user.get('id'),
                 'city': user.get('city').get('title'),
                 'city_id': user.get('city').get('id'),
                 'sex': user.get('sex'),
                 'age': bdate_to_age(user.get('bdate'))}

    return user_info

print(get_user_info(api,user_id))

def build_search_params(api,user_id):
    """Получаем параметры поиска"""
    user_info = get_user_info(api,user_id)
    if user_info.get('age') is None or user_info.get('city_id') is None or user_info.get('sex') == 0:
        return None
    if user_info.get('sex') == 2:
        sex = 1
    elif user_info.get('sex') == 1:
        sex = 2
    city_id = user_info.get('city_id')
    age_from = user_info.get('age') - 5
    age_to = user_info.get('age') + 5
    return {'sex': sex, 'city': city_id, 'age_from': age_from, 'age_to': age_to, 'has_photo': 1, 'count': 10, 'fields': 'has_photo,city,sex,bdate'}

def build_profile_url(person: dict) -> str:
    screen_name = person.get('screen_name')
    if screen_name:
        return f"https://vk.com/{screen_name}"
    return f"https://vk.com/id{person['id']}"

def search_candidates(api,user_id):
    """Получаем список кандидатов"""
    # candidate = api.users.search(q=0,sex=2,count = 10, city=city_id,age_from=20,age_to=25,has_photo=1,fields='has_photo,city,sex,bdate')
    candidates = api.users.search(**build_search_params(api,user_id))
    candidates_info = []
    for candidate in candidates['items']:
        if candidate.get('sex')==2:
            gender = 'мужской'
        elif candidate.get('sex')==1:
            gender = 'женский'
        else:
            gender = ''
        age = bdate_to_age(candidate.get('bdate'))
        if age is None:
            continue
        person_info = {
            'candidate_id':candidate.get('id'),
            'name':candidate.get('first_name'),
            'surname':candidate.get('last_name'),
            'sex':candidate.get('sex'),
            'gender':gender,
            'age':age,
            'city':candidate.get('city',{}).get('title'),
            'link': build_profile_url(candidate)
        }
        candidates_info.append(person_info)
    return candidates_info

print(search_candidates(api,user_id))

# candidate_photo = api.photos.get(owner_id=73463924, album_id='profile',rev=0,extended=1)
# print(candidate_photo)

def get_3_candidate_photo(api,candidate_id):
    try:
        response = api.photos.get(owner_id=candidate_id, album_id='profile',rev=0,extended=1)
        all_photos = response.get('items')
    except vk_f.exceptions.ApiError:
        return []

    top_3_photos = sorted(all_photos,key=lambda x: x['likes']['count'],reverse=True)[:3]
    result = []
    for photo in top_3_photos:
        att = f'photo{photo["owner_id"]}_{photo["id"]}'
        if photo.get('access_key'):
            att += f"_{photo['access_key']}"
        result.append(att)
    return result

print(get_3_candidate_photo(api,73463924))
