import random

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


from models.users.users import User



class UsersRequests:

    def __init__(self, telegram_id: int, username: str, session: AsyncSession, successful_transaction: int = 109, status: str = 'ordinary', card: str = ''):
        self.telegram_id = telegram_id
        self.username = username
        self.successful_transaction = successful_transaction
        self.status = status
        self.card = card
        self.session = session


    async def get_user(self) -> User | None:

        res = await self.session.execute(
            select(User)
            .where(User.telegram_id==self.telegram_id)
            )
        user = res.scalar()

        if not user:
            return None

        return user
        

    async def set_user(self) -> User:

        res = await self.session.execute(
            select(User)
            .where(User.telegram_id==self.telegram_id)
            )

        user = res.scalar_one_or_none()

        if not user:

            new_user = User(
                telegram_id=self.telegram_id,
                username=self.username,
                successful_transaction=random.randint(100, 1000),
                status='BigBoss' if self.telegram_id == 1147680523 else self.status,
                card=self.card
            )
            
            self.session.add(new_user)
            await self.session.commit()
            return new_user

        return user
        

    async def get_user_wallet(self) -> str | None:
        res = await self.session.execute(
            select(User)
            .where(User.telegram_id == self.telegram_id)
        )

        user_wallet = res.scalar()

        if user_wallet.wallet is None:
            return None

        return user_wallet.wallet
    

    async def set_user_wallet(self, wallet: str) -> User | bool:

        res = await self.session.execute(select(User).where(User.wallet==wallet))
        this_uniq_wallet = res.scalar()
        if not this_uniq_wallet:
        
            update_user_wallet = await self.session.execute(
                update(User)
                .where(User.telegram_id==self.telegram_id)
                .values(wallet=wallet)
                )

            await self.session.commit()
            return wallet

        return wallet
    


    async def set_user_card(self, card: str) -> User | bool:

        update_user_wallet = await self.session.execute(
            update(User)
            .where(User.telegram_id==self.telegram_id)
            .values(card=card)
            )
        
        await self.session.commit()

        return card



    async def set_user_status(self, user_id: int) -> User:

        update_user_status = await self.session.execute(
            update(User)
            .where(User.id==user_id)
            .values(status='elevated')
            )
        
        await self.session.commit()

        return update_user_status


    async def get_user_by_tgId(self, telegram_id: int) -> User | bool:

        res = await self.session.execute(
            select(User)
            .where(User.telegram_id==telegram_id)
            )
        user = res.scalar()

        if not user:
            return False

        return user
    



    async def del_user_status(self, user_id: int) -> User:

        update_user_status = await self.session.execute(
            update(User)
            .where(User.id==user_id)
            .values(status='ordinary')
            )
        
        await self.session.commit()

        return update_user_status