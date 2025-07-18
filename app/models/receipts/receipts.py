from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from core.database.base import Base



class Receipts(Base):

    __tablename__ = 'receipts'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    id_receipt: Mapped[str] = mapped_column(nullable=False, unique=True)
    tovar: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[str] = mapped_column(nullable=False)

    buyer: Mapped[int] = mapped_column(nullable=True, default=None)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="receipts")


