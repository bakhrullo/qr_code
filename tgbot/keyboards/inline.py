from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

Add = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Qo\'shish ✅', callback_data='add'),
                                            InlineKeyboardButton('Ortga 🔙', callback_data='back'))

Back = InlineKeyboardMarkup().add(InlineKeyboardButton('Ortga 🔙', callback_data='back'))
