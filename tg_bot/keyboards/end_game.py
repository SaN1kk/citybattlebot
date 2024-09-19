from aiogram import types


def get_end_game_keyboard():
    btn_1 = types.KeyboardButton(text="🏳️ Сдаться")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[btn_1]], resize_keyboard=True)
    return keyboard
