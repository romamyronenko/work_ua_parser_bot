import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, LinkPreviewOptions

from utils import prettify_job
from work_ua_parser import get_jobs


class States(StatesGroup):
    ENTER_CITY = State()


TOKEN = getenv("BOT_TOKEN")

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: "FSMContext") -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    await change_city(message, state)


@router.message(Command("change_city"))
async def change_city(message: Message, state: "FSMContext") -> None:
    await message.answer("enter new city")
    await state.set_state(States.ENTER_CITY)


@router.message(States.ENTER_CITY)
async def enter_city(message: Message, state: "FSMContext") -> None:
    await message.answer(f'city changed to {message.text}')
    await state.set_data({'city': message.text})
    await state.set_state(None)


@router.message()
async def echo_handler(message: Message, state: "FSMContext") -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
        data = await state.get_data()
        city = data.get('city')
        await message.answer(f'Your_city: {city}')
        jobs = get_jobs(message.text, city)
        for job in jobs:
            await message.answer(prettify_job(job), link_preview_options=LinkPreviewOptions(is_disabled=True))
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
