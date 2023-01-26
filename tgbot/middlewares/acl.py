# from typing import Optional
#
# from aiogram import types
# from aiogram.dispatcher.handler import CancelHandler
# from aiogram.dispatcher.middlewares import BaseMiddleware
#
#
# class ACLMiddleware(BaseMiddleware):
#
#     async def setup_chat(self, data: dict, user: types.User, message: types.message = None,
#                          chat: Optional[types.Chat] = None):
#        admin_id =
#         if user.id not in admin_id:
#             get_res = await get_user(user.id)
#             if 'detail' in get_res:
#                 data['user'] = False
#                 await create_user(user.id, user.first_name, user.username)
#             else:
#                 data['user'] = True
#                 data['user_info'] = get_res
#                 data['admins_id'] = admin_id
#                 if get_res['is_banned']:
#                     raise CancelHandler()
#
#     async def setup_chat_for_query(self, data: dict, user: types.User, chat: Optional[types.Chat] = None):
#         get_admin_res = await get_admin()
#         admin_id = []
#         data['admins_id'] = admin_id
#         for i in get_admin_res:
#             admin_id.append(i['admin_id'])
#         if user.id not in admin_id:
#             get_res = await get_user(user.id)
#             data['user_info'] = get_res
#             print(get_res)
#             if get_res['is_banned']:
#                 raise CancelHandler()
#
#     async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
#         await self.setup_chat_for_query(data=data, user=query.from_user,
#                                         chat=query.message.chat if query.message else None)
#
#     async def on_pre_process_message(self, message: types.Message, data: dict):
#         await self.setup_chat(data=data, user=message.from_user, message=message)
