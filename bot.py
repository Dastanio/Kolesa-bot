import logging
import config

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter

import asyncio
from datetime import datetime

from Pars import KolesaKz

#Задаем уровень логов
logging.basicConfig(level=logging.INFO)

#Инициализируем бота
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('db.db')

sg = KolesaKz('lastkey.txt')


# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, True)
	
	await message.answer("Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")

# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
		db.add_subscriber(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")

#Тест таймера
async def schedule(wait_for):
 	while True:
  		await asyncio.sleep(wait_for)

  		# получаем список подписчиков бота
  		subscriptions = db.get_subscriptions()

  		# отправляем всем новость
  		for i in sg.new_cars():
   			for s in subscriptions:
				   await bot.send_message(s[1], 'Новая машина: ' + i, disable_notification=True)

#Запускаем лонг полинг
if __name__==  '__main__':
	dp.loop.create_task(schedule(600))
	executor.start_polling(dp,skip_updates=True)