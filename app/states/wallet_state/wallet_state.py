from aiogram.fsm.state import StatesGroup, State


class WalletReg(StatesGroup):
    card = State()
    address_wallet = State()