from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from selenium import webdriver
import pandas as pd
import dbworker

from config import token
from parser_logic import parse_page, find_miners, get_miner_info

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Список майнеров", "Подписаться на обновления"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Выберите нужное вам действие на кнопках ниже:", reply_markup=keyboard)


@dp.message_handler(Text(equals="Список майнеров"))
async def get_all_miners(message: types.Message):
    dbworker.set_state(message.chat.id, "Список")
    from config import link, delay, driver_path
    await bot.send_message(message.chat.id, "Подождите, файл генерируется...")
    driver = webdriver.Chrome(executable_path=driver_path)

    html = parse_page(link, driver, delay)

    lines = find_miners(html)
    miners = dict()

    for line in lines:
        if get_miner_info(line):
            link, miner_dict = get_miner_info(line)
            if link is not None and miner_dict is not None:
                miners[link[:-1]] = miner_dict

    df = pd.DataFrame(data=miners, index=['Mining group', 'Token', 'Fees',
                                          'Age', 'Daily', 'TVL', 'Evol TVL'
                                          ])

    df = df.T
    filename = 'miners.xlsx'
    df.to_excel(filename)
    file = open(filename, 'rb')

    await bot.send_document(message.chat.id, file)


@dp.message_handler(Text(equals="Подписаться на обновления"))
async def subscribe(message: types.Message):
    await bot.send_message(message.chat.id, "Пожалуйста, введите частоту загрузки обновлений (в минутах)")
    dbworker.set_state(message.chat.id, "Подписка")


@dp.message_handler(lambda message: dbworker.get_current_state(message.chat.id) == "Подписка")
async def subscribe_user(message: types.Message):
    if message.text.isnumeric():
        await bot.send_message(message.chat.id, f"Вы будете получать обновления каждые {message.text} минут.")
    else:
        await bot.send_message(message.chat.id, f"Вы ввели неверное число. Попробуйте снова")


if __name__ == '__main__':
    executor.start_polling(dp)
