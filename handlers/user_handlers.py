from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

# Инициализируем роутер уровня модуля
router = Router()

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='ПРИВЕТ!')
