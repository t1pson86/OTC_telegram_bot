from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



class InlineKeyboardReceipt():

    def __init__(self):

        self.inlkey_receipt = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='❌ Отменить сделку', callback_data='Cancel_the_deal')],
            ])
        
        self.create_wallet = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🪙 Добавить кошелек', callback_data='wallet')],
            ])
        
        self.yes_receipt = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='✅ Подтвердить выполнение', callback_data='confirm')],
            ])
        

receipt_button = InlineKeyboardReceipt()