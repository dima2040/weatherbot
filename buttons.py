from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class ButtonFilter(CallbackData, prefix =  'btn') :
    lat: float
    lon: float


def make_keyboard(cities):
    buttons = list()
    for index, city in enumerate(cities):
        buttons.append(
            InlineKeyboardButton(
                text=str(index+1), 
                callback_data=ButtonFilter(
                    lat=city['latitude'], lon=city['longitude']
                ).pack()
            )
        )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
             buttons,
        ]
    )
    return markup
