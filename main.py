import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from handlers import user_handlers
from handlers.other_handlers import send_message_cron, turn_check
from apscheduler.schedulers.asyncio import AsyncIOScheduler


# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')
    dp = Dispatcher()


    # Обнуление признака проведения проверки
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        turn_check,
        trigger='interval',
        minutes = 2,
        start_date=datetime.now().replace(hour=23, minute=40),
        end_date=datetime.now().replace(hour=23, minute=55),
        kwargs={'bot': bot, 'group_id': config.tg_group_id}
        )
    scheduler.start()

    # Сообщения по расписанию
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        send_message_cron,
        trigger='interval',
        minutes = 2,
        start_date=datetime.now().replace(hour=7, minute=30),
        end_date=datetime.now().replace(hour=8, minute=45),
        kwargs={'bot': bot, 'group_id': config.tg_group_id}
        )
    scheduler.start()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())