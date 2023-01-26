from aiogram import Dispatcher
from aiogram.types import Message
from sqlalchemy import select

from tgbot.db.model import Info


async def user_start(m: Message):
    arg = m.get_args()
    if len(arg) != 0:
        db_session = m.bot.get("db")
        try:
            async with db_session() as session:
                data = await session.execute(select(Info).where(Info.id == int(arg)))
                res = data.scalars()
            for i in res:
                await m.answer(f"👤 Ism: {i.name}\n"
                               f"👨 Familiya: {i.surname}\n"
                               f"📞 Telefon raqam: {i.number}\n"
                               f"👨‍💻 Soxa: {i.job}")
        except ValueError:
            await m.answer('Iltimos Qr kodni skaner qiling!')
    else:
        await m.answer('Iltimos Qr kodni skaner qiling!')


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
