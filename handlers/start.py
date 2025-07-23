from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import settings

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Я бот времени!")
