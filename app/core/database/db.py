from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.configuration.settings import db_settings


class SessionInfo():



    def __init__(self):
        self.engine = create_async_engine(
            url=f'sqlite+aiosqlite:///{db_settings.DB_NAME}',
            echo=False)
        self.async_session = async_sessionmaker(
                                bind = self.engine,
                                class_ = AsyncSession,
                                expire_on_commit = False
                                )
        

new_async_session = SessionInfo()