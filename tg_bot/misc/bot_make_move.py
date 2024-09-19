import random

from tg_bot.misc.get_last_valid_letter import get_last_valid_letter


def bot_make_move(chat_id, valid_cities, user_city):
    from bot import db
    last_letter = get_last_valid_letter(user_city)

    available_cities = [city for city in valid_cities if
                        city.startswith(last_letter) and not db.is_city_used(chat_id, city)]

    if available_cities:
        return random.choice(available_cities)
    return None
