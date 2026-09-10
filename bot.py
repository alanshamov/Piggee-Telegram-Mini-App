import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN", "ВСТАВЬ_СВОЙ_ТОКЕН_СЮДА")
APP_URL = os.getenv("APP_URL", "https://alanshamov.github.io/Piggee-Telegram-Mini-App/kopilka.html")
# На Render адрес выглядит так: https://<имя>-<рандом>.onrender.com
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

HELLO_TEXT = (
    "\U0001F437 Привет! Я Piggee — твоя цифровая копилка.\n\n"
    "Создай таблицу ячеек как на твоей настоящей копилке, "
    "зачёркивай ячейку, когда кладёшь деньги, — и следи за прогрессом в процентах.\n\n"
    "Нажми кнопку ниже, чтобы открыть копилку \u2193"
)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="\U0001F437 Открыть копилку",
                    web_app=WebAppInfo(url=APP_URL),
                )
            ]
        ]
    )
    await message.answer(HELLO_TEXT, reply_markup=keyboard)


async def handle_update(request: web.Request):
    update = await request.json()
    await dp.feed_update(bot, update)
    return web.Response()


async def main():
    if not BOT_TOKEN or "ВСТАВЬ" in BOT_TOKEN:
        raise SystemExit("Задай BOT_TOKEN в переменных окружения")
    if not WEBHOOK_HOST:
        raise SystemExit("Задай WEBHOOK_HOST (URL приложения на Render)")

    await bot.delete_webhook(drop_pending_updates=False)
    await bot.set_webhook(url=f"{WEBHOOK_HOST}/webhook")

    app = web.Application()
    app.router.add_post("/webhook", handle_update)
    port = int(os.getenv("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()
    print(f"Бот запущен, webhook: {WEBHOOK_HOST}/webhook")
    await asyncio_forever()


async def asyncio_forever():
    import asyncio
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
