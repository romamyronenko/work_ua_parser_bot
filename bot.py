import asyncio
import logging
import pickle
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    LinkPreviewOptions,
)

from utils import prettify_job
from work_ua_parser import get_jobs


class States(StatesGroup):
    ENTER_CITY = State()


TOKEN = getenv("BOT_TOKEN")

router = Router()


def set_data(user_id, data_):
    try:
        with open("user_data.p", "rb") as f:
            data = pickle.loads(f.read())
    except:
        data = {}
    data[user_id] = data_
    with open("user_data.p", "wb") as f:
        pickle.dump(data, f)


def get_data(user_id, key):
    try:
        with open("user_data.p", "rb") as f:
            data = pickle.loads(f.read())
    except:
        data = {}
    return data.get(user_id, {}).get(key)


@router.message(CommandStart())
async def command_start_handler(message: Message, state: "FSMContext") -> None:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="change_city"),
                KeyboardButton(text="start"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=keyboard
    )

    # await change_city(message, state)


@router.message(Command("change_city"))
async def change_city(message: Message, state: "FSMContext") -> None:
    await message.answer("enter new city")
    await state.set_state(States.ENTER_CITY)


@router.message(States.ENTER_CITY)
async def enter_city(message: Message, state: "FSMContext") -> None:
    await message.answer(f"city changed to {message.text}")
    set_data(message.from_user.id, {"city": message.text})

    await state.set_state(None)


class TextFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: "Message") -> bool:
        return message.text == self.my_text


@router.message(TextFilter("change_city"))
async def change_city(message: Message, state: "FSMContext") -> None:
    await message.answer("enter new city")
    await state.set_state(States.ENTER_CITY)


@router.message()
async def echo_handler(message: Message, state: "FSMContext") -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
        city = get_data(message.from_user.id, "city")
        await message.answer(f"Your_city: {city}")
        jobs = get_jobs(message.text, city)
        for job in jobs:
            await message.answer(
                prettify_job(job),
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Start bot."),
            types.BotCommand(command="change_city", description="Update current city."),
        ]
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
