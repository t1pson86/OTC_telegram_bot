from core.configuration.settings import app_settings

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from states.receipt_state.receipt_state import ReceiptReg
from keyboards.main_keyboard.main_keyboard import welcome_button
from keyboards.receipt_keyboard.receipt_keyboard import receipt_button
from core.security.generation import uniq_generation
from requests.users_requests.users import UsersRequests
from requests.receipts_requests.receipts import ReceiptsRequests


router = Router()

bot = Bot(token=app_settings.TOKEN)





@router.callback_query(F.data == 'deal')
async def cmd_create_receipt(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
) -> str:

    await callback.answer('deal') 


    user = UsersRequests(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        session=session
    )

    user_now = await user.get_user()

    if user_now.wallet and user_now.card == 'RU':

        await state.set_state(ReceiptReg.price)

        await bot.delete_message(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id
            )

        return await callback.message.answer_photo(photo='AgACAgEAAxkBAAICQWhnyjBbWnJemRLd15P-Llv4eRxqAALUrjEbdlpBR4tKeV52AiIkAQADAgADeAADNgQ',
caption="""💼 <b>Создание сделки</b>

Введите сумму RUB сделки в формате: 100.5""",

reply_markup=welcome_button.wallet_inlkey,
parse_mode='HTML'
)

    if user_now.wallet and user_now.card == 'TON':

        await state.set_state(ReceiptReg.price)

        await bot.delete_message(
            chat_id=callback.message.chat.id, 
            message_id=callback.message.message_id
            )

        return await callback.message.answer_photo(photo='AgACAgEAAxkBAAICQWhnyjBbWnJemRLd15P-Llv4eRxqAALUrjEbdlpBR4tKeV52AiIkAQADAgADeAADNgQ',
caption="""💼 <b>Создание сделки</b>

Введите сумму TON сделки в формате: 100.5""",

reply_markup=welcome_button.wallet_inlkey,
parse_mode='HTML'
)

    await bot.delete_message(
        chat_id=callback.message.chat.id, 
        message_id=callback.message.message_id
        )

    return await callback.message.answer_photo(photo='AgACAgEAAxkBAAICQWhnyjBbWnJemRLd15P-Llv4eRxqAALUrjEbdlpBR4tKeV52AiIkAQADAgADeAADNgQ', caption='Для создания сделки необходимо добавить кошелек!', reply_markup=receipt_button.create_wallet)



@router.message(ReceiptReg.price)
async def cmd_set_price(
    message: Message,
    state: FSMContext
) -> str:
    try:
        new_sum = int(message.text)

        await state.update_data(
            price = message.text
        )

        await state.set_state(ReceiptReg.tovar)

        return await message.answer(
"""📝 <b>Укажите, что вы предлагаете в этой сделке:</b>

Пример: 10 Кепок и Пепе...""",

reply_markup=welcome_button.wallet_inlkey,
parse_mode='HTML'
)
    except Exception as e:
        return await message.answer('❌ Неверный формат суммы. Попробуйте еще раз.')



@router.message(ReceiptReg.tovar)
async def cmd_set_tovar(
    message: Message,
    state: FSMContext,
    session: AsyncSession
) -> str:
    
    await state.update_data(
        tovar = message.text
    )

    user = UsersRequests(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        session=session
    )

    this_user = await user.set_user()

    data = await state.get_data()

    id_receipt = uniq_generation()

    receipt = ReceiptsRequests(
        id_receipt=id_receipt,
        tovar=data["tovar"],
        price=data["price"],
        user_id=this_user.id,
        session=session
    )

    new_created_receipt = await receipt.create_receipt()

    await state.clear()

    if this_user.card == 'RU':

        return await message.answer(
f"""
✅ <b>Сделка успешно создана!</b>

💰 <b>Сумма:</b> {new_created_receipt.price} RUB
📜 <b>Описание:</b> {new_created_receipt.tovar}
🔗 <b>Ссылка для покупателя:</b> https://t.me/{app_settings.BOT_NAME}?start={id_receipt}
""",

reply_markup=receipt_button.inlkey_receipt,
parse_mode="HTML"
)

    if this_user.card == 'TON':

        return await message.answer(
f"""
✅ <b>Сделка успешно создана!</b>

💰 <b>Сумма:</b> {new_created_receipt.price} TON
📜 <b>Описание:</b> {new_created_receipt.tovar}
🔗 <b>Ссылка для покупателя:</b> https://t.me/{app_settings.BOT_NAME}?start={id_receipt}
""",

reply_markup=receipt_button.inlkey_receipt,
parse_mode="HTML"
)




@router.callback_query(F.data == "Cancel_the_deal")
async def cmd_cancle_the_deal(
    callback: CallbackQuery,
    session: AsyncSession
) -> str:

    await callback.answer('Cancel_the_deal')

    user_res = UsersRequests(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        session=session
    )

    user = await user_res.get_user()

    if user:

        receipt = ReceiptsRequests(
            user_id=user.id,
            session=session
        )

        this_receipt = await receipt.get_receipt_by_user_id()

        if this_receipt:

            if this_receipt.buyer:

                await bot.send_message(
                    chat_id=this_receipt.buyer,
                    text=f'Сделка #{this_receipt.id_receipt} была отменена продавцом @{this_receipt.user.username}!'
                    )

                await bot.send_photo(
                    photo='AgACAgEAAxkBAAICQWhnyjBbWnJemRLd15P-Llv4eRxqAALUrjEbdlpBR4tKeV52AiIkAQADAgADeAADNgQ',
                    chat_id=this_receipt.buyer,
                    caption="""
<b>Добро пожаловать в ELF OTC – надежный P2P-гарант</b>

💼 <b>Покупайте и продавайте всё, что угодно – безопасно!</b>
От Telegram-подарков и NFT до токенов и фиата – сделки проходят легко и без риска.

🔹 Удобное управление кошельками

📖 <b>Как пользоваться?</b>
Ознакомьтесь с инструкцией — https://telegra.ph/OTC-06-29

Выберите нужный раздел ниже:""",

reply_markup=welcome_button.inlkey,
parse_mode='HTML'
)

                await callback.message.answer(f'Сделка #{this_receipt.id_receipt} отменена!')

                await callback.message.answer_photo(photo='AgACAgEAAxkBAAICQWhnyjBbWnJemRLd15P-Llv4eRxqAALUrjEbdlpBR4tKeV52AiIkAQADAgADeAADNgQ',
caption="""
<b>Добро пожаловать в ELF OTC – надежный P2P-гарант</b>

💼 <b>Покупайте и продавайте всё, что угодно – безопасно!</b>
От Telegram-подарков и NFT до токенов и фиата – сделки проходят легко и без риска.

🔹 Удобное управление кошельками

📖 <b>Как пользоваться?</b>
Ознакомьтесь с инструкцией — https://telegra.ph/OTC-06-29

Выберите нужный раздел ниже:""",
reply_markup=welcome_button.inlkey,
parse_mode='HTML'
)

                del_user = await receipt.delete_receipt(id_receipt=this_receipt.id_receipt)

                return

        return await callback.message.answer('❌ Данная сделка не активна!')