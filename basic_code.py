from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv('VK_TOKEN')
user_id = os.getenv('ID')
app_id = os.getenv('APP_ID')
token = os.getenv('TOKEN')

# token = input('Token:vk1.a.87MWTt2NUgNM5T58PqpIbCjXmS851M38MTMNuioWP6rmUJLRbBKXXEsjlobUHch2IPcBBJe9Xk8NoGqMLv3D7Af_9_a8KAUKAiel7angFkGpdgscbHxvmr8jWqG9ER_NoKhlw2apqaENAdDhvwnFLsn-HA_9d_HYiHu21KfYKi4s7FrYMIJ6Fn7WHS5inH9rJqyt5V4FNb2NlJY2vj7Vlw')

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk,wait=25)

def write_msg(user_id, message):
    response = vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})
    return response

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text.lower().strip()
            if request in ("привет","начать","старт"):
                write_msg(event.user_id, f'Хай, {event.user_id}. Я бот, который поможет тебе с'
                                         f' поиском второй половины.Напиши "Поиск", чтобы начать или "Помощь",'
                                         f'чтобы узнать больше')
                if request == "помощь":
                    write_msg(event.user_id, "Описание функций")  #TODO: написать блок с описанием функций бота
                elif request == "поиск":                                  # TODO:Основная логика бота
                    pass
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
                break
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")