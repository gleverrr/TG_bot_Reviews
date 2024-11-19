from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from tg_bot.handlers import register_handlers
from config import Config
async def main():
    BOT_TOKEN = Config.BOT_TOKEN
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
