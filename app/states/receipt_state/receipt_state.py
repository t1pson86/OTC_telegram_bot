from aiogram.fsm.state import StatesGroup, State


class ReceiptReg(StatesGroup):
    price = State()
    tovar = State()
    