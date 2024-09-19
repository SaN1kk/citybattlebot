from aiogram import types

difficulty_menu = {
    "easy": "🟢 Лёгкая (Города мира)",
    "medium": "🟡 Средняя (Города СНГ)",
    "hard": "🔴 Сложная (Города России)"
}


def get_difficulty_menu():
    btn_1 = types.InlineKeyboardButton(text="🟢 Лёгкая (Города мира)", callback_data="difficulty_easy")
    btn_2 = types.InlineKeyboardButton(text="🟡 Средняя (Города СНГ)", callback_data="difficulty_medium")
    btn_3 = types.InlineKeyboardButton(text="🔴 Сложная (Города России)", callback_data="difficulty_hard")
    btn_4 = types.InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="back_to_menu")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [btn_1],
        [btn_2],
        [btn_3],
        [btn_4]
    ])
    return keyboard
