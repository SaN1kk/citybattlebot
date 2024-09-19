from aiogram import types


def create_welcome_keyboard():
    btn_1 = types.InlineKeyboardButton(text="▶️ Начать игру", callback_data="start_game")
    btn_2 = types.InlineKeyboardButton(text="🏆 Таблица рекордов", callback_data="leaderboard")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [btn_1],
        [btn_2]
    ])
    return keyboard
