import asyncio
import logging
import os

import requests
from aiogram.enums.content_type import ContentType
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from .buttons import make_keyboard, ButtonFilter
from .utils import EMOJI_FLAGS


logging.basicConfig(level=logging.INFO)

load_dotenv()
api_token = os.environ.get("ECHOBOT_API_TOKEN")

bot = Bot(token=api_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Привет!👋🏼")


async def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,precipitation&daily=sunrise,sunset&timezone=Europe/Moscow&forecast_days=1"
    resp = requests.get(url)
    data = resp.json()
    temp = data['current']['temperature_2m']
    wind = data['current']['wind_speed_10m']
    sunrise = data['daily']['sunrise'][0].split('T')[1]
    sunset = data['daily']['sunset'][0].split('T')[1]
    precipitation = data['current']['precipitation']
    return data, temp, wind, sunrise, sunset, precipitation


@dp.message(F.content_type == ContentType.LOCATION)
async def on_geolocation(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude

    data, temp, wind, sunrise, sunset, precipitation =  await get_weather(lat, lon)
    await message.reply(f'Температура: {temp}°с\n'
                        f'Ветер: {wind} м\с\n'
                        f'Восход: {sunrise}☀️\n'
                        f'Закат: {sunset}🌙\n'
                        f'Осадки {precipitation}☁️' )


@dp.callback_query(ButtonFilter.filter())
async def on_pick_city(query: types.CallbackQuery, callback_data: ButtonFilter):
    lat = callback_data.lat
    lon = callback_data.lon
    data, temp, wind, sunrise, sunset, precipitation = await get_weather(lat, lon)
    await query.message.delete_reply_markup()
    await query.message.edit_text(
        f'Температура: {temp}°с\n'
        f'Ветер: {wind} м\с\n'
        f'Восход: {sunrise}☀️\n'
        f'Закат: {sunset}🌙\n'
        f'Осадки {precipitation}☁️'
    )


@dp.message()
async def on_message(message: types.Message):
    name = message.text
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={name}&count=3&language=ru&format=json"
    resp = requests.get(url)
    data = resp.json()
    text = f"Результаты поиска: {name}\n\n"
    for city in data['results']:
        emoji_name = city['country_code'].lower()
        if emoji_name in EMOJI_FLAGS.keys():
            emoji = EMOJI_FLAGS[emoji_name]
        else:   
            emoji = emoji_name.upper() + '/'
        text += f"{emoji}{city['name']}\n"
        try:
            text += f"\t\tНаселение: {city['population']}\n\n"
        except:
            text += "\n\n"

    await message.reply(text, reply_markup=make_keyboard(data['results']))


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
