import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import os
from dotenv import load_dotenv
from tg_bot_reviews.tg_bot.handlers.handlers import register_handlers


async def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if BOT_TOKEN is None:
        print("BOT_TOKEN not found in .env file")
        raise ValueError("BOT_TOKEN not found in .env file")
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    register_handlers(dp, bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
