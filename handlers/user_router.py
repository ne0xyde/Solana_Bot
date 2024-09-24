import numbers
import re
from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from create_bot import bot
from db_handler.db_funk import get_user_data, insert_user, get_solana_address, update_solana_address
from solana.solana_wallet import create_solana_wallet, get_solana_balance, send_solana_to_wallet
from keyboards.kbs import main_kb, profile_page_kb, wallet_page
from utils.utils import get_refer_id


user_router = Router()

universe_text = ('To get information about your profile, use the ‘My Profile’ button or a special command '
                 'from the command menu.')


# класс состояния
class ChatState(StatesGroup):
    user_message = State()  # Состояние для хранения сообщения пользователя
    bot_message = State()  # Состояние для хранения сообщения бота


# Класс состояния отслеживания процесса изменения кошелька
class WalletEvents(StatesGroup):
    waiting_for_new_wallet = State()
    my_wallet_balance = State()
    target_address = State()
    target_value = State()


# функция обработки удаления сообщений
async def delete_previous_messages(message: Message, state: FSMContext):
    data = await state.get_data()
    user_message_id = data.get('user_message_id')
    bot_message_id = data.get('bot_message_id')
    if user_message_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=user_message_id)
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")
    await state.clear()


# функция валидации введённого кошелька
def validate_solana_address(address: str) -> bool:
    return len(address) < 46 and address.isalnum()


# функция валидации введённой суммы
def validate_balance(balance):
    return re.findall(r'^[+]?((\d+(\.\d*)?)|(\.\d+))$', fr'{balance}')


# хендлер команды старт
@user_router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, state: FSMContext):
    await state.update_data(user_message_id=message.message_id)
    await delete_previous_messages(message, state)
    user_info = await get_user_data(user_id=message.from_user.id)
    if user_info:
        for user in user_info:
            if user.solana_address is not None:
                sol_balance = await get_solana_balance(user.solana_address)
                response_text = (f"Welcome back {user.full_name},\n"
                                 f"Your solana wallet:\n `{user.solana_address}`\n"
                                 f"you're wallet balance is `{sol_balance}` SOL,\n"
                                 f"{universe_text}"
                                 )
            else:
                solana_address = await get_solana_address(message.from_user.id)
                response_text = (f"Welcome back {user.full_name},\n"
                                 f"Your solana wallet:\n `{solana_address}`\n"
                                 f"Before starting trading, please send some SOL to your Solana wallet address,\n"
                                 f"{universe_text}"
                                 )
    else:
        refer_id = get_refer_id(command.args)
        mnemonic, solana_address, private_key = await create_solana_wallet()
        await insert_user(user_data={
            'user_id': message.from_user.id,
            'full_name': message.from_user.full_name,
            'user_login': message.from_user.username,
            'solana_address': solana_address,
            'privateKey': private_key,
            'mnemonic': mnemonic,
            'refer_id': refer_id
        })
        response_text = (f'{message.from_user.full_name}, we are glad you have joined us! Welcome!'
                         f'Your new solana wallet:\n `{solana_address}`\n'
                         'Before starting trading, please send some SOL to your Solana wallet address, '
                         )
        if refer_id != 'None':
            response_text.join(f'you are a referral of a user with ID <b>{refer_id}</b>. {universe_text}')
        response_text.join(f'{universe_text}')
    bot_reply = await message.answer(text=response_text, reply_markup=main_kb(message.from_user.id))
    await state.update_data(bot_message_id=bot_reply.message_id)


# хендлер кнопки назад
@user_router.message(F.text.contains('Back'))
async def cmd_back(message: Message, state: FSMContext):
    await state.update_data(user_message_id=message.message_id)
    await delete_previous_messages(message, state)
    bot_reply = await message.answer(f"{message.from_user.first_name}, you're already in my database. {universe_text}",
                                     reply_markup=main_kb(message.from_user.id))
    await state.update_data(bot_message_id=bot_reply.message_id)


# хендлер команды обновить информацию о кошельке
@user_router.message(Command('refresh'))
@user_router.message(F.text.contains('Refresh'))
async def cmd_refresh(message: Message, state: FSMContext):
    await state.update_data(user_message_id=message.message_id)
    await delete_previous_messages(message, state)
    solana_address = await get_solana_address(message.from_user.id)
    sol_balance = await get_solana_balance(solana_address)
    bot_reply = await message.answer(f"Your Solana wallet: `{solana_address}`\n"
                                     f"you're wallet balance is `{sol_balance}` SOL",
                                     reply_markup=wallet_page(message.from_user.id))
    await state.update_data(bot_message_id=bot_reply.message_id)


# хендлер команды обновить информацию о кошельке
@user_router.message(Command('wallet'))
@user_router.message(F.text.contains('My wallet'))
async def cmd_refresh(message: Message, state: FSMContext):
    await state.update_data(user_message_id=message.message_id)
    await delete_previous_messages(message, state)
    solana_address = await get_solana_address(message.from_user.id)
    sol_balance = await get_solana_balance(solana_address)
    bot_reply = await message.answer(f"Your Solana wallet: **{solana_address}**\n"
                                     f"you're wallet balance is `'{sol_balance}'` SOL",
                                     reply_markup=wallet_page(message.from_user.id))
    await state.update_data(bot_message_id=bot_reply.message_id)


# хендлер команды замены кошелька на свой
@user_router.message(Command('change_wallet'))
@user_router.message(F.text.contains('Change my wallet address'))
async def cmd_change_wallet(message: Message, state: FSMContext):
    await state.update_data(user_message_id=message.message_id)
    await delete_previous_messages(message, state)
    solana_address = await get_solana_address(message.from_user.id)
    sol_balance = await get_solana_balance(solana_address)
    bot_reply = await message.answer(f"Your Solana wallet: **{solana_address}**\n"
                                     f"you're wallet balance is `'{sol_balance}'` SOL,\n"
                                     f"Please enter your new Solana wallet address:",
                                     reply_markup=wallet_page(message.from_user.id))
    await state.update_data(bot_message_id=bot_reply.message_id)
    await state.set_state(WalletEvents.waiting_for_new_wallet)


# хендлер обработки введённого нового адреса
@user_router.message(WalletEvents.waiting_for_new_wallet)
async def process_new_wallet_address(message: Message, state: FSMContext):
    new_wallet_address = message.text

    # Проверим валидность введённого адреса (можно добавить более сложную проверку)
    if not validate_solana_address(new_wallet_address):
        await message.answer("The address you provided is invalid. Please try again.")
        return

    # Обновляем адрес в базе данных
    await update_solana_address(message.from_user.id, new_wallet_address)

    await state.clear()

    await message.answer(f"Your Solana wallet address has been successfully updated to: `{new_wallet_address}`",
                         reply_markup=wallet_page(message.from_user.id))


# хендлер профиля
@user_router.message(Command('profile'))
@user_router.message(F.text.contains('My profile'))
async def get_profile(message: Message, state: FSMContext):
    await state.update_data(user_message_id=message.message_id)
    await delete_previous_messages(message, state)
    text = (f'👉 Your Telegram ID: <code><b>{message.from_user.id}</b></code>\n'
            f'🚀 Your personalised invitation link: '
            f'<code>https://t.me/test_solana_robot?start={message.from_user.id}</code>')
    bot_reply = await message.answer(text, reply_markup=profile_page_kb(message.from_user.id))
    await state.update_data(bot_message_id=bot_reply.message_id)


# хендлер отправки монет на другой кошелёк
@user_router.message(Command('send_sol'))
@user_router.message(F.text.contains('Send SOL to wallet'))
async def cmd_send_sol(message: Message, state: FSMContext):
    await state.update_data(user_message_id=message.message_id)
    await delete_previous_messages(message, state)
    solana_address = await get_solana_address(message.from_user.id)
    sol_balance = await get_solana_balance(solana_address)
    bot_reply = await message.answer(f"Your Solana wallet: {solana_address}\n"
                                     f"you're wallet balance is {sol_balance} SOL,\n"
                                     f"Please enter the wallet address to send:",
                                     reply_markup=main_kb(message.from_user.id))
    await state.update_data(bot_message_id=bot_reply.message_id)
    await state.set_state(WalletEvents.target_address)


# хендлер обработки введённого нового адреса
@user_router.message(WalletEvents.target_address)
async def capture_wallet_address(message: Message, state: FSMContext):
    await state.update_data(user_message_id=message.message_id)
    await delete_previous_messages(message, state)

    target_wallet_address = message.text

    # Проверим валидность введённого адреса (можно добавить более сложную проверку)
    if not validate_solana_address(target_wallet_address):
        await message.answer("The address you provided is invalid. Please try again.",
                             reply_markup=main_kb(message.from_user.id))
        return

    await state.update_data(target_address=message.text)
    data = await state.get_data()
    print(f'capture_wallet_address data = {data}\n type = {type(data)}')
    bot_reply = await message.answer('Done! Now send the amount to send:')
    await state.update_data(bot_message_id=bot_reply.message_id)
    await state.set_state(WalletEvents.target_value)


# хендлер обработки введённой суммы для отправки
@user_router.message(WalletEvents.target_value)
async def capture_balance(message: Message, state: FSMContext):
    await state.update_data(user_message_id=message.message_id)
    # await delete_previous_messages(message, state)

    # Проверим введённую сумму
    if not validate_balance(message.text):
        await message.answer("The entered amount is not valid. Please try again.",
                             reply_markup=main_kb(message.from_user.id))
        return

    await state.update_data(target_value=message.text)
    data = await state.get_data()
    print(f'capture_balance data = {data}\n type = {type(data)}')
    # отправляем указанную сумму на адрес

    reply = await send_solana_to_wallet(message.from_user.id, data.get("target_address"), data.get("target_value"))
    # reply = "None else"
    bot_reply = await message.answer(f'You try to send {data.get("target_value")} SOL from your wallet to:\n'
                                     f'{data.get("target_address")}\n'
                                     f'reply is {reply}',
                                     reply_markup=main_kb(message.from_user.id)
                                     )
    await delete_previous_messages(message, state)
    await state.update_data(bot_message_id=bot_reply.message_id)
    await state.clear()
