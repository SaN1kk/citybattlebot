import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from parser_all import get_cites_all
from parser_ru import get_cites_ru
from parser_sng import get_cites_sng
from tg_bot.config import load_config
from tg_bot.db.sqlite import DataBase

from tg_bot.handlers import start

logger = logging.getLogger(__name__)
config = load_config(path=".env")
bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode="HTML"))

db = DataBase()

cites_ru = get_cites_ru()
cites_sng = get_cites_sng()
cites_all = get_cites_all()


async def main():
    logging.basicConfig(level=logging.INFO,
                        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(message)s')

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(start.router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("БОТ ОСТАНОВИЛСЯ!")
