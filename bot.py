import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Update, Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN", "ВСТАВЬ_СВОЙ_ТОКЕН_СЮДА")
APP_URL = os.getenv("APP_URL", "https://alanshamov.github.io/Piggee-Telegram-Mini-App/kopilka.html")
# На Render адрес выглядит так: https://<имя>-<рандом>.onrender.com
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "")
# Баннер для приветствия — лежит в репозитории, раздаётся через GitHub Pages
BANNER_URL = os.getenv("BANNER_URL", "https://alanshamov.github.io/Piggee-Telegram-Mini-App/banner-piggee-github.jpg")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

HELLO_TEXT = (
    "\U0001F4B0 Привет! Я Piggee — твоя цифровая копилка.\n\n"
    "Копилка физическая, а «цифровая копия» — это я: "
    "слежу за прогрессом, не портя настоящую.\n\n"
    "\U0001F4A1 Что я умею:\n"
    "\u2022 создавать копилку — как таблицу на твоей коробке;\n"
    "\u2022 зачёркивать ячейку, когда кладёшь деньги;\n"
    "\u2022 сам считать накопленное, цель и прогресс в %.\n\n"
    "\u2B07\U0001F447 Нажми кнопку и начинай копить!"
)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="\U0001F4B0 Открыть копилку",
                    web_app=WebAppInfo(url=APP_URL),
                )
            ]
        ]
    )
    caption = HELLO_TEXT
    try:
        await message.answer_photo(photo=BANNER_URL, caption=caption, reply_markup=keyboard)
    except Exception:
        await message.answer(caption, reply_markup=keyboard)


async def handle_update(request: web.Request):
    data = await request.json()
    update = Update.model_validate(data)
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
