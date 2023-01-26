from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

MainMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Exceldan yuklash 📋'),
                                                         KeyboardButton('Alohida qo\'shish 📥'))

Remove = ReplyKeyboardRemove()
