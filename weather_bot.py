
import telebot, sys, logging, requests, json, datetime, telebot_calendar, math, pyowm
from pyowm import timeutils
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from mysql.connector import errorcode
from telebot import types, apihelper
from mysql.connector import errorcode
import mysql.connector
from string import Template
from telebot import apihelper

bot = telebot.TeleBot('909567963:AAFknxY2mtLa1cfBnO3C9KzRmSb3001L4HM')
owm = pyowm.OWM('945a394890eab9e4e54bdda87d5e37e7', language="ru")  # Сюда вставляем ключ OWM


@bot.message_handler(commands=["start"])
def geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение, для получения сведений о погоде",
                     reply_markup=keyboard)



@bot.message_handler(content_types=["location"])
def location(message):

        #message.text = "Норильск"
        #obs = owm.weather_at_place(message.text)
        bot.delete_message(message.chat.id, message.message_id)
        #fc = owm.three_hours_forecast(message.location.latitude, message.location.longitude)#каждые 3 часа отправка сообщения о погоде
        obs = owm.weather_at_coords(message.location.latitude, message.location.longitude)
        # obs = owm.weather_at_place(message.text)  # Тут мы передаем название города которое пишем в боте.
        w = obs.get_weather()  # поулчаем всю погоду из этого города
        temp = w.get_temperature('celsius')[
            "temp"]  # time=2020-04-06 00:18:51+00, status=snow, detailed status=небольшой снегопад
        temp_max = w.get_temperature('celsius')["temp_max"]  # максимальная температура воздуха
        temp_min = w.get_temperature('celsius')["temp_min"]  # минимальная температура воздуха
        wind = w.get_wind()["speed"]  # скорость ветра
        status = w.get_detailed_status()  # Указывает например снегопад\дождь
        humidity = w.get_humidity()  # влажность
        cloud = w.get_clouds()  # облачность
        rain = w.get_rain()  # дождь
        snow = w.get_snow()  # снег
        sunrise_time = w.get_sunrise_time('iso')  # Время восхода
        sunset_time = w.get_sunset_time('iso')  # Время заказа

        t = round(temp)

        answer = f"В городе сейчас {str(status)}\n\n"  # .format( message.text, str(status))
        answer += f"Температура ~ {t}°C \n"
        # answer += f"Макс. {temp_max}°C \n"
        # answer += f"Мин. {temp_min}°C \n"
        answer += f"Влажность {humidity}% \n"
        answer += f"Облачность {cloud}%\n"
        answer += f"Скорость ветра составляет {wind} м/с \n\n"
        # answer += f"Восход {sunrise_time}\n"
        # answer += f"Закат {sunset_time}\n"
        # answer += f"Дождь {rain}\n"
        # answer += f"Снег {snow}\n\n"

        if t <= 10:
            answer += "На улице холодно, одевайся теплее!\n"
        elif t <= 18:
            answer += "На улице прохладно, захвати с собой кофту!\n"
        elif t <= 25:
            answer += "На улице тепло, иди гуляй!\n"
        else:
            answer += "На улице жара!\n"

        if str(status) == "дождь":
            answer += "Не забудь зонт, ты же не хочешь промокнуть?"
        elif str(status) == "легкий дождь":
            answer += "Зонт возьми, вдруг польет сильнее?"
        elif str(status) == "пасмурно" and (humidity > 50):
            answer += "Возможен дождь, но это не точно"

        bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)