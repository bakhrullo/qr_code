import os

import qrcode
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InputFile, CallbackQuery
from aiogram.utils.deep_linking import get_start_link

from tgbot.db.model import Info
from tgbot.keyboards.reply import *
from tgbot.keyboards.inline import *
from tgbot.misc.get_info import get_information
from tgbot.misc.states import *


async def admin_start(m: Message):
    await m.reply("Salom admin! 👋", reply_markup=MainMenu)
    await AdminMain.main.set()


async def send_example(m: Message):
    await m.answer("Iltimos faylni manashu ko\'rinishda yuboring! 📩", reply_markup=Remove)
    await m.bot.send_document(m.from_user.id, document=InputFile('example.xlsx'), reply_markup=Back)
    await AdminEx.get_file.set()


async def get_file(m: Message):
    file_name = str(m.from_user.id)
    await m.document.download(destination_file=f'{file_name}.xlsx')
    await m.answer('Iltimos biroz kutib turing')
    await m.answer('⏳')
    res = await get_information(file_name, m)
    if res:
        await m.answer('dwdwd')
    else:
        await m.answer('Xato formatda yuborildi. Iltimos qayta tekshirib yuboring. ❌', reply_markup=Back)


async def req_name(m: Message):
    await m.answer('Ismni yuboring', reply_markup=Back)
    await AdminAdd.get_name.set()


async def get_name(m: Message, state: FSMContext):
    await state.update_data(name=m.text)
    await m.answer('Familiyani yuboring', reply_markup=Back)
    await AdminAdd.get_surname.set()


async def get_surname(m: Message, state: FSMContext):
    await state.update_data(surname=m.text)
    await m.answer('Raqmani yuboring', reply_markup=Back)
    await AdminAdd.get_number.set()


async def get_number(m: Message, state: FSMContext):
    await state.update_data(number=m.text)
    await m.answer('Soxani yuboring', reply_markup=Back)
    await AdminAdd.get_job.set()


async def get_job(m: Message, state: FSMContext):
    await state.update_data(job=m.text)
    data = await state.get_data()
    await m.answer(f"👤 Ism: {data['name']}\n"
                   f"👨 Familiya: {data['surname']}\n"
                   f"📞 Telefon raqam: {data['number']}\n"
                   f"👨‍💻 Soxa: {data['job']}", reply_markup=Add)
    await AdminAdd.get_add.set()


async def add(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db_session = c.bot.get("db")
    try:
        async with db_session() as session:
            ses = await session.merge(
                Info(name=data['name'], surname=data['surname'], number=data['number'],
                     job=data['job']))
            await session.commit()
            link = await get_start_link(ses.id)
            img = qrcode.make(link)
            img.save(f"{ses.id}")
            await c.bot.send_photo(c.from_user.id, photo=InputFile(f"{ses.id}"),
                                   caption=f"👤 Ism: {ses.name}\n"
                                           f"👨 Familiya: {ses.surname}\n"
                                           f"📞 Telefon raqam: {ses.number}\n"
                                           f"👨‍💻 Soxa: {ses.job}", reply_markup=MainMenu)
            os.remove(f"{ses.id}")
            await AdminMain.main.set()
    except:
        err = f"Faylda {data['number']} nomer takrorlanyapti"
        await c.answer(err)
        return False


async def back(c: CallbackQuery):
    await c.message.delete()
    await c.message.answer("Salom admin! 👋", reply_markup=MainMenu)
    await AdminMain.main.set()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(send_example, Text(equals='Exceldan yuklash 📋'), state=AdminMain.main, is_admin=True)
    dp.register_message_handler(req_name, Text(equals='Alohida qo\'shish 📥'), state=AdminMain.main, is_admin=True)
    dp.register_message_handler(get_name, state=AdminAdd.get_name, is_admin=True)
    dp.register_message_handler(get_surname, state=AdminAdd.get_surname, is_admin=True)
    dp.register_message_handler(get_number, state=AdminAdd.get_number, is_admin=True)
    dp.register_message_handler(get_job, state=AdminAdd.get_job, is_admin=True)
    dp.register_message_handler(get_file, content_types=types.ContentTypes.DOCUMENT, state=AdminEx.get_file, is_admin=True)
    dp.register_callback_query_handler(add, Text(equals='add'), state=AdminAdd.get_add, is_admin=True)
    dp.register_callback_query_handler(back, Text(equals='back'), state="*", is_admin=True)
