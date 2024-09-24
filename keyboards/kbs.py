from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins


def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="💰 My wallet")],
        [KeyboardButton(text="👤 My profile")],
        [KeyboardButton(text="🔁 Refresh")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Admin panel")])
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Menu:"
    )


def profile_page_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="💰 My wallet")],
        [KeyboardButton(text="🔙 Back")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Admin panel")])
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Menu:"
    )


def wallet_page(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="👛 Change my wallet address")],
        [KeyboardButton(text="↔️ Send SOL to wallet")],
        [KeyboardButton(text="🔁 Refresh")],
        [KeyboardButton(text="🔙 Back")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Admin panel")])
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Menu:"
    )
