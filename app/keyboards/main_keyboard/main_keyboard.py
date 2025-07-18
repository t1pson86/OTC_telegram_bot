from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class InlineKeyboardMain():

    def __init__(self):

        self.inlkey = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🪙 Добавить/изменить кошелек', callback_data='wallet')],
            [InlineKeyboardButton(text='📄 Создать сделку', callback_data='deal')],
            [InlineKeyboardButton(text='📞 Поддержка', url='https://t.me/p2p_vsedela')]])
        
        self.wallet_inlkey = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🔙 Вернуться в меню', callback_data='back')]])
        
        self.inlkey_card = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🇷🇺 RUB', callback_data='RUS')],
            [InlineKeyboardButton(text='💎 TON', callback_data='TONS')],
            [InlineKeyboardButton(text='🔙 Вернуться в меню', callback_data='back')],
            ])
        

welcome_button = InlineKeyboardMain()