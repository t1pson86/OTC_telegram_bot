from aiogram import BaseMiddleware

from core.database.db import new_async_session


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with new_async_session.async_session() as session:
            data["session"] = session
            return await handler(event, data)