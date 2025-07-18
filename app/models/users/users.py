from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base



class User(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    telegram_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    username: Mapped[str] = mapped_column(nullable=False)
    successful_transaction: Mapped[int] = mapped_column(nullable=False, default=109)
    status: Mapped[str] = mapped_column(nullable=False, default='ordinary')
    card: Mapped[str] = mapped_column(nullable=False, default='')
    wallet: Mapped[str] = mapped_column(default=None, nullable=True, unique=True)

    receipts: Mapped["Receipts"] = relationship(back_populates="user", cascade="all, delete-orphan")