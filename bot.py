# language: Python, file: bot.py
import os
import threading
import asyncio
import logging
from flask import Flask

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from modules import phone, email, company, debts, court, domain, leak

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/")
@app.route("/health")
def health():
    return "OK", 200

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(msg: Message):
    await msg.answer(
        "<b>OSINT-бот — открытые источники</b>\n\n"
        "/phone &lt;номер&gt;\n"
        "/email &lt;почта&gt;\n"
        "/company &lt;ИНН&gt;\n"
        "/debts &lt;ФИО, дата&gt;\n"
        "/court &lt;ИНН&gt;\n"
        "/domain &lt;домен&gt;\n"
        "/username &lt;ник&gt;\n"
        "/leak &lt;почта/номер&gt;\n",
        parse_mode=ParseMode.HTML,
    )

@dp.message(Command("phone"))
async def cmd_phone(msg: Message):
    args = msg.text.split(maxsplit=1)
    if len(args) < 2:
        return await msg.answer("формат: /phone +79991234567")
    await msg.answer(await phone.lookup(args[1].strip()))

@dp.message(Command("email"))
async def cmd_email(msg: Message):
    args = msg.text.split(maxsplit=1)
    if len(args) < 2:
        return await msg.answer("формат: /email test@example.com")
    await msg.answer(await email.lookup(args[1].strip()))

@dp.message(Command("company"))
async def cmd_company(msg: Message):
    args = msg.text.split(maxsplit=1)
    if len(args) < 2:
        return await msg.answer("формат: /company 7707083893")
    await msg.answer(await company.lookup(args[1].strip()))

@dp.message(Command("debts"))
async def cmd_debts(msg: Message):
    args = msg.text.split(maxsplit=1)
    if len(args) < 2:
        return await msg.answer("формат: /debts Иванов Иван Иванович, 01.01.1990")
    await msg.answer(await debts.lookup(args[1].strip()))

@dp.message(Command("court"))
async def cmd_court(msg: Message):
    args = msg.text.split(maxsplit=1)
    if len(args) < 2:
        return await msg.answer("формат: /court 7707083893")
    await msg.answer(await court.lookup(args[1].strip()))

@dp.message(Command("domain"))
async def cmd_domain(msg: Message):
    args = msg.text.split(maxsplit=1)
    if len(args) < 2:
        return await msg.answer("формат: /domain example.com")
    await msg.answer(await domain.lookup(args[1].strip()))

@dp.message(Command("username"))
async def cmd_username(msg: Message):
    args = msg.text.split(maxsplit=1)
    if len(args) < 2:
        return await msg.answer("формат: /username nickname")
    await msg.answer(await domain.username_lookup(args[1].strip()))

@dp.message(Command("leak"))
async def cmd_leak(msg: Message):
    args = msg.text.split(maxsplit=1)
    if len(args) < 2:
        return await msg.answer("формат: /leak test@example.com")
    await msg.answer(await leak.lookup(args[1].strip()))


async def run_bot():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


def start_bot_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())


if __name__ == "__main__":
    threading.Thread(target=start_bot_thread, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
