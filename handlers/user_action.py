from aiogram import Router
from aiogram.types import Message
from schemas import UserActionCreateSchema, UserActionDTOSchema
from repository import UserActionRepo
from database.database import get_async_session

from utils.to_ics import ToCalendar


router = Router()


@router.message()
async def add_user_action(message: Message):
    user_a_create = UserActionCreateSchema(
        user_tg_id=message.from_user.id,
        action=message.text,
    )

    user_a_repo = UserActionRepo()
    async with get_async_session() as session:
        await session.begin()

        last_user_action = await user_a_repo.get_by_filter_from_end(
            session=session,
            limit=1,
            user_tg_id=user_a_create.user_tg_id,
        )
        if len(last_user_action) > 0:
            last_user_action = last_user_action[0]
            await user_a_repo.set_stop(
                session=session, uuid=last_user_action.uuid, stop=True
            )

            await session.flush()

            last_user_action = await user_a_repo.get_by_filter_from_end(
                session=session,
                limit=1,
                user_tg_id=user_a_create.user_tg_id,
            )
            last_user_action = last_user_action[0]

            calendar = ToCalendar()
            await calendar.update_user_ics(
                UserActionDTOSchema(
                    user_tg_id=last_user_action.user_tg_id,
                    action=last_user_action.action,
                    create_at=last_user_action.create_at,
                    update_at=last_user_action.update_at,
                )
            )

        await user_a_repo.add(session=session, action_data=user_a_create)

        await session.commit()

    await message.reply("Успешно добавленно!")
