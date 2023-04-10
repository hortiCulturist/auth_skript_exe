import aiogram.types
from aiogram import Bot
from aiogram.dispatcher import Dispatcher, filters, FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

import bot_button
import bot_config
import server_db
import key_generator

storage = MemoryStorage()
bot = Bot(bot_config.TOKEN)
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('Bot is running')


class LicenseTimeState(StatesGroup):
    hour = State()


class LicenseKeysState(StatesGroup):
    waiting_for_key_count = State()


@dp.message_handler(commands='start', user_id=bot_config.ADMIN_ID)
async def strt(message: types.Message):
    await bot.send_message(message.from_user.id, text="KeyGen 🔑", reply_markup=bot_button.start_button())


#  начало "Время лицензии"
@dp.message_handler(text='Изменить время лицензии ⏳', user_id=bot_config.ADMIN_ID)
async def change_license_time(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите количество дней:')
    await LicenseTimeState.hour.set()


@dp.message_handler(state=LicenseTimeState.hour)
async def set_license_time(message: types.Message, state: FSMContext):
    days = int(message.text)
    server_db.add_license_time(days)
    await bot.send_message(message.chat.id, f'Время лицензии установлено\nКоличество дней: {days}', reply_markup=bot_button.start_button())
    await state.finish()
#  конец "Время лицензии"


@dp.message_handler(text='Сгенерировать ключи 🔑', user_id=bot_config.ADMIN_ID)
async def generate_keys_handler(message: types.Message):
    await bot.send_message(message.from_user.id, 'Введите количество ключей: ')
    await LicenseKeysState.waiting_for_key_count.set()


@dp.message_handler(state=LicenseKeysState.waiting_for_key_count)
async def generate_keys(message: types.Message, state: FSMContext):
    key_count = message.text.strip()
    if not key_count.isdigit():
        await message.reply('Введите число!')
        return
    key_count = int(key_count)
    keys = key_generator.key_gen(key_count)
    await bot.send_message(message.from_user.id, f'Вот ваши {key_count} ключей:\n\n' + '\n'.join(keys),
                           reply_markup=bot_button.start_button())
    await state.finish()


@dp.message_handler(text='Показать все ключи 📋', user_id=bot_config.ADMIN_ID)
async def generate_keys_handler(message: types.Message):
    key_strings = [str(key[1]) for key in server_db.all_keys()]
    result = "\n".join(key_strings)
    await bot.send_message(message.from_user.id, f'{result}')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
