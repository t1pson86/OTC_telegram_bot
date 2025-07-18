from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional


from models.receipts.receipts import Receipts

class ReceiptsRequests:

    def __init__(self, session: AsyncSession, id_receipt: str = None, tovar: str = None, price: str = None,  user_id: int = None, buyer: str = None):
        self.id_receipt = id_receipt
        self.tovar = tovar
        self.price = price
        self.buyer = buyer
        self.user_id = user_id
        self.session = session



    async def get_receipt(self) -> Receipts | None:

        res = await self.session.execute(
            select(Receipts)
            .where(Receipts.id_receipt==self.id_receipt)
            .options(selectinload(Receipts.user))
        )

        this_receipt = res.scalar()

        if not this_receipt:
            return None


        return this_receipt



    async def get_receipt_by_user_id(self) -> Receipts | None:

        res = await self.session.execute(
            select(Receipts)
            .where(Receipts.user_id==self.user_id)
            .options(selectinload(Receipts.user))
        )

        this_receipt = res.scalar()

        if this_receipt:

            return this_receipt
        
        return None



    async def create_receipt(self) -> Receipts | bool:

        res = await self.session.execute(
            select(Receipts)
            .where(Receipts.id_receipt==self.id_receipt)
            )
        
        receipt = res.scalar_one_or_none()

        if receipt:
            new_receipt = Receipts(
                id_receipt=self.id_receipt[:-2] + '8q',
                tovar=self.tovar,
                price=self.price,
                buyer=self.buyer,
                user_id=self.user_id
            )

            self.session.add(new_receipt)

            await self.session.commit()

            return new_receipt
        
        new_receipt = Receipts(
            id_receipt=self.id_receipt,
            tovar=self.tovar,
            price=self.price,
            buyer=self.buyer,
            user_id=self.user_id
        )

        self.session.add(new_receipt)

        await self.session.commit()
        
        return new_receipt



    async def update_buyer_info(self) -> bool:

        updt_receipt_buyer_info = await self.session.execute(
            update(Receipts)
            .where(Receipts.id_receipt==self.id_receipt)
            .values(buyer=self.buyer)
        )

        await self.session.commit()

        return True



    async def delete_receipt(self, id_receipt):

        del_user = await self.session.execute(
            delete(Receipts)
            .where(Receipts.id_receipt==id_receipt)
        )

        await self.session.commit()

        return True