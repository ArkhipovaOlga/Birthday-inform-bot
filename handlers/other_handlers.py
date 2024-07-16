from aiogram import Bot
from datetime import date, datetime
from services.bd import bd
from services.vars import vars

async def send_message_cron(bot:Bot, group_id:int):
    if vars['check'] == 0:
        for day in bd.keys():
            parsed_day = datetime.strptime(day, '%Y-%m-%d').date().replace(year=date.today().year)
            if parsed_day == date.today():
                await bot.send_message(group_id, f'Сегодня день рождения {bd[day]}! Поздравляем!')
                await bot.set_chat_title(group_id, title= f'С днем рождения, {bd[day]}!')

    vars['check'] = 1

async def turn_check(bot:Bot, group_id:int):
    if vars['check'] == 1:
        vars['check'] = 0
        await bot.set_chat_title(group_id, title=vars['group_name'])