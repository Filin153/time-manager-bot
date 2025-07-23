from database.models import UserActionORM
from schemas import UserActionCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, desc


class UserActionRepo:
    @staticmethod
    async def add(session: AsyncSession, action_data: UserActionCreateSchema):
        user_a_orm = UserActionORM(
            **action_data.model_dump()
        )
        session.add(user_a_orm)
        return user_a_orm
    
    @staticmethod
    async def set_stop(session: AsyncSession, uuid: str, stop: bool):
        query = update(UserActionORM).values(stop=stop).where(UserActionORM.uuid == uuid)
        await session.execute(query)
        return True
    
    @staticmethod
    async def get_by_filter(session: AsyncSession, limit: int = 10, offset: int = 0, **kwargs) -> list[UserActionORM]:
        query = select(UserActionORM).filter_by(**kwargs).offset(offset)

        if limit != -1:
            query = query.limit(limit)

        res = await session.execute(query)
        res = res.scalars().all()
        return res
    
    @staticmethod
    async def get_by_filter_from_end(session: AsyncSession, limit: int = 10, offset: int = 0, **kwargs) -> list[UserActionORM]:
        query = select(UserActionORM).order_by(desc(UserActionORM.create_at)).filter_by(**kwargs).offset(offset)

        if limit != -1:
            query = query.limit(limit)

        res = await session.execute(query)
        res = res.scalars().all()
        return res