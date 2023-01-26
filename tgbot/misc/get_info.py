import asyncio
import os

import openpyxl
import qrcode
from aiogram.types import Message, InputFile
from aiogram.utils.deep_linking import get_start_link

from tgbot.db.model import Info


async def get_information(file_name, m: Message):
    book = openpyxl.load_workbook(file_name + '.xlsx', read_only=True)
    sheet = book.active
    if sheet['A1'].value is None:
        return False
    db_session = m.bot.get("db")
    try:
        async with db_session() as session:
            for i in range(2, sheet.max_row + 1):
                if sheet[f'E{i}'].value is not None:
                    ses = await session.merge(
                        Info(name=sheet[f'C{i}'].value, surname=sheet[f'D{i}'].value, number=str(sheet[f'E{i}'].value),
                             job=sheet[f'F{i}'].value))
                    await session.commit()
                    link = await get_start_link(ses.id)
                    img = qrcode.make(link)
                    img.save(f"{ses.id}")
                    await m.bot.send_photo(m.from_user.id, photo=InputFile(f"{ses.id}"),
                                           caption=f"👤 Ism: {ses.name}\n"
                                                   f"👨 Familiya: {ses.surname}\n"
                                                   f"📞 Telefon raqam: {ses.number}\n"
                                                   f"👨‍💻 Soxa: {ses.job}")
                    os.remove(f"{ses.id}")
                    await asyncio.sleep(1)
                else:
                    err = f'Faylda E{i} bo\'sh'
                    await m.answer(err)
                    return False
    except:
        err = f"Faylda {sheet[f'E{i}'].value} nomer takrorlanyapti"
        await m.answer(err)
        return False
    return True
