import asyncio
from logs import setup_logging
from create_bot import dp, bot
from handlers import start_router, user_action_router
from middleware import AccessMiddleware

setup_logging()


async def main():
    dp.message.middleware(AccessMiddleware())

    dp.include_router(start_router)
    dp.include_router(user_action_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
