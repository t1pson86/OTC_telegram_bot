import asyncio

from core.configuration.settings import app_settings

from aiogram import Bot, Dispatcher

from routers.main_router.main_router import router
from routers.receipts_router.receipts_router import router as router_receipts
from routers.admins_router.admins_router import router as router_admins

from core.database.db import new_async_session
from core.database.base import Base
from core.middleware.users_middleware.users import DbSessionMiddleware



bot = Bot(token=app_settings.TOKEN)
dp = Dispatcher()
dp.update.middleware(DbSessionMiddleware())


async def create_db():
    async with new_async_session.engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)



async def main():
    await create_db()
    dp.include_router(router)
    dp.include_router(router_receipts)
    dp.include_router(router_admins)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')