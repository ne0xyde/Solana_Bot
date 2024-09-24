from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db_handler.db_funk import get_all_users, count_referrals
from handlers.user_router import ChatState, delete_previous_messages
from create_bot import (admins,
                        bot)
from keyboards.kbs import profile_page_kb

admin_router = Router()


@admin_router.message((F.text.contains('Admin panel')) & (F.from_user.id.in_(admins)))
async def get_profile(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        await state.update_data(user_message_id=message.message_id)
        await delete_previous_messages(message, state)
        try:
            all_users_data = await get_all_users(count=False)
            admin_text = (
                f'👥 The database contains <b>{len(all_users_data)}</b> users. Brief information:\n\n'
            )

            for user in all_users_data:
                admin_text += (
                    f'👤 Telegram ID: {user.user_id}\n'
                    f'📝 Full name: {user.full_name}\n'
                )

                if user.user_login is not None:
                    admin_text += f'🔑 Login: {user.user_login}\n'

                if user.refer_id is not None:
                    admin_text += f'👨‍💼 Was invited by: {user.refer_id}\n'
                referrals_count = await count_referrals(user.user_id)
                admin_text += (
                    f'👥 Has referrals: {referrals_count} users\n'
                    f'\n〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\n'
                )
        except Exception as ex:
            print(f'Exception is ====> {ex}')
        bot_reply = await message.answer(admin_text, reply_markup=profile_page_kb(message.from_user.id))
        await state.update_data(bot_message_id=bot_reply.message_id)
