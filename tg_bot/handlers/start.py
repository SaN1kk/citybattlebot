from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from tg_bot.keyboards.end_game import get_end_game_keyboard
from tg_bot.keyboards.get_difficulty import get_difficulty_menu, difficulty_menu
from tg_bot.keyboards.welcome import create_welcome_keyboard
from tg_bot.misc.bot_make_move import bot_make_move
from tg_bot.misc.get_last_valid_letter import get_last_valid_letter

router = Router()


# /start
@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text="👋 Добро пожаловать в игру <b>'Города'</b>!", reply_markup=create_welcome_keyboard())


# Начало игры
@router.callback_query(lambda call: call.data == "start_game")
async def choose_difficulty(call: CallbackQuery):
    await call.message.edit_text(text="☑️ Выберите <b>уровень сложности</b>:", reply_markup=get_difficulty_menu())
    await call.answer()


# Возвращение в меню
@router.callback_query(lambda call: call.data == "back_to_menu")
async def back_to_menu(call: CallbackQuery):
    await call.message.edit_text(text="👋 Добро пожаловать в игру <b>'Города'</b>!",
                                 reply_markup=create_welcome_keyboard())
    await call.answer()


# Таблица рекордов
@router.callback_query(lambda call: call.data == "leaderboard")
async def display_leaderboard(call: CallbackQuery):
    from bot import db
    chat_id = call.message.chat.id
    top_games = db.get_top_5_games(chat_id=chat_id)
    response = "<b>Лучшие 5 игр по количеству введённых городов:</b>\n\n"

    for rank, (chat_id, city_count, created_at) in enumerate(top_games, start=1):
        response += f"🏆 <b>Место {rank}</b> - <i>Дата создания: {created_at}</i>\n" \
                    f"🌟 <b>Городов названо:</b> {city_count}\n\n"

    await call.message.edit_text(text=response,
                                 reply_markup=types.InlineKeyboardMarkup(
                                     inline_keyboard=[
                                         [types.InlineKeyboardButton(text="⬅️ Вернуться назад",
                                                                     callback_data="back_to_menu")]
                                     ]))
    await call.answer()


# Начало игры после выбора сложности
@router.callback_query(lambda call: call.data.startswith("difficulty_"))
async def difficulty_selection(call: CallbackQuery):
    from bot import db
    difficulty = call.data.split("_")[1]
    chat_id = call.message.chat.id
    if db.is_game_active(chat_id=chat_id):
        await call.answer(text="У вас уже есть активная игра. Пожалуйста, завершите текущую игру перед началом новой.",
                          show_alert=True)
        return

    db.create_new_game(chat_id=chat_id, difficulty=difficulty)
    await call.message.answer(text=f"✅ Игра начата с уровнем сложности <b>{difficulty_menu[difficulty]}</b>. Ваш ход!",
                              reply_markup=get_end_game_keyboard())
    await call.answer()
    await call.message.delete()


# Сдаться
@router.message(F.text == "🏳️ Сдаться")
async def surrender(message: Message):
    from bot import db
    chat_id = message.chat.id
    if not db.is_game_active(chat_id=chat_id):
        await message.answer("❌ У вас нет активной игры.")
        return

    city_count = db.get_city_count(chat_id=chat_id)
    db.end_game(chat_id=chat_id)
    await message.answer(f"🏳️ Вы сдались. Игра завершена.\n\nКоличество городов в игре: <b>{city_count}</b>",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(text="👋 Добро пожаловать в игру <b>'Города'</b>!", reply_markup=create_welcome_keyboard())


# Обработка логики игры
@router.message(F.text)
async def handle_city_input(message: Message):
    from bot import db, cites_all, cites_sng, cites_ru
    chat_id = message.chat.id
    city = message.text.strip().title()
    city = city.replace("Ё", "Е").replace("ё", "е")

    if not db.is_game_active(chat_id=chat_id):
        await message.answer(text="⚠️ У вас нет активной игры.\nНачните новую игру с команды /start.")
        print(db.is_game_active(chat_id))
        return

    if db.is_city_used(chat_id=chat_id, city=city):
        await message.answer(text=f"⚠️ Город <b>{city}</b> уже был использован в этой игре.\nНазовите другой город.")
        return

    if db.get_game_current_turn(chat_id=chat_id) == "bot":
        await message.answer(f"⚠️ Сейчас не Ваш ход, дождитесь пока сходит бот!")
        return

    difficulty = db.get_game_difficulty(chat_id=chat_id)
    if difficulty == 'easy':
        valid_cities = cites_all
    elif difficulty == 'medium':
        valid_cities = cites_sng
    elif difficulty == 'hard':
        valid_cities = cites_ru
    else:
        await message.answer("❌ Ошибка при определении сложности игры.")
        print(difficulty)
        return

    city_variants = [city.lower(), city.replace("-", ' ').lower(), city.replace(' ', '-').lower()]
    city_found = False
    for city_variant in city_variants:
        if city_variant in (c.lower() for c in valid_cities):
            city_found = True
            break

    if not city_found:
        await message.answer(
            f"⚠️ Город <b>{city}</b> не найден в списке городов для текущей сложности. Назовите другой город.")
        return

    if db.get_last_bot_city(chat_id=chat_id):
        last_letter = get_last_valid_letter(db.get_last_bot_city(chat_id))
        if message.text[0].upper() != last_letter:
            await message.answer(
                f"⚠️ Город должен начинаться с буквы <b>{last_letter}</b>")
            return

    await message.answer(f"✅ Вы назвали город <b>{city}</b>\nБоту на букву <b>{get_last_valid_letter(city)}</b>")
    db.create_new_move(chat_id=chat_id, player_type='player', city=city)

    bot_city = bot_make_move(chat_id, valid_cities, city)
    if bot_city:
        db.create_new_move(chat_id=chat_id, player_type='bot', city=bot_city)
        await message.answer(
            f"🤖 Бот выбрал город <b>{bot_city}</b>\nВам на букву <b>{get_last_valid_letter(bot_city)}</b>")
    else:
        db.end_game(chat_id=chat_id)
        await message.answer("❌ Бот не смог найти подходящий город. Игра завершена.",
                             reply_markup=ReplyKeyboardRemove())
        await message.answer(text="👋 Добро пожаловать в игру <b>'Города'</b>!", reply_markup=create_welcome_keyboard())
