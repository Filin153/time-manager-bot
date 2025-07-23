from aiogram import BaseMiddleware
from aiogram.types import Message

from config import settings

from typing import Callable, Dict, Any, Awaitable


class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.from_user.id not in settings.ALLOW_USER_IDS:
            await event.answer(f"Нет доступа\n\nВаш ID -> {event.from_user.id}")
            return
        
        return await handler(event, data)
