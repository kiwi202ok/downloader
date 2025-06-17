import aiogram
import os
import dotenv
import asyncio


dotenv.load_dotenv()

bot = aiogram.Bot(os.getenv("bot_token"))
dp = aiogram.Dispatcher()


def on_start():
     print("bot ishladi...")

async def main():
     dp.startup.register(on_start)
     await dp.start_polling(bot)

asyncio.run(main())