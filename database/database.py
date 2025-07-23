from contextlib import asynccontextmanager, contextmanager
from datetime import datetime

from sqlalchemy import create_engine, DateTime, func, UUID, text
from sqlalchemy import event, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped
from sqlalchemy.orm import Session
import uuid

from config import settings

engine_async = create_async_engine(settings.PG_ASYNC_URL)
engine_sync = create_engine(settings.PG_SYNC_URL)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def uuid(csl) -> Mapped[uuid.UUID]:
        return mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("uuid_generate_v7()")
        )

    @declared_attr
    def create_at(cls) -> Mapped[datetime]:
        return mapped_column(DateTime(timezone=True), server_default=func.now())

    @declared_attr
    def update_at(cls) -> Mapped[datetime]:
        return mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    @declared_attr
    def delete_at(cls) -> Mapped[datetime]:
        return mapped_column(DateTime(timezone=True), nullable=True)


@asynccontextmanager
async def get_async_session() -> AsyncSession:
    async with AsyncSession(engine_async) as conn:
        yield conn


@contextmanager
def get_sync_session() -> Session:
    with Session(engine_sync) as conn:
        yield conn


def apply_soft_delete_filter(query):
    # Получаем все сущности, участвующие в запросе
    entities = [desc['entity'] for desc in query.column_descriptions if desc['entity']]

    # Проверяем, есть ли у сущностей столбец deleted_at
    for entity in entities:
        if entity is None:
            continue

        # Получаем модель из отношения, если это relationship
        model = entity.class_ if hasattr(entity, 'class_') else entity

        if hasattr(model, 'deleted_at'):
            # Добавляем фильтр deleted_at.is_(None)
            deleted_at_filter = model.deleted_at.is_(None)

            if query.whereclause is None:
                query = query.filter(deleted_at_filter)
            else:
                query = query.filter(and_(deleted_at_filter, query.whereclause))

    return query


@event.listens_for(Session, "do_orm_execute")
def soft_delete_filter(execute_state):
    if not execute_state.is_select:
        return  # Применяем только к SELECT-запросам

    # Пропускаем системные и служебные запросы
    if execute_state.is_column_load or execute_state.is_relationship_load:
        return

    # Проверяем флаг для отключения фильтра
    if execute_state.execution_options.get('include_deleted', False):
        return

    # Модифицируем запрос
    execute_state.statement = apply_soft_delete_filter(execute_state.statement)


# @event.listens_for(Session, 'before_flush')
# def before_flush_listener(session, flush_context, instances):
#     for obj in session.deleted:
#         if hasattr(obj, 'deleted_at'):
#             obj.deleted_at = datetime.utcnow()
#             session.expunge(obj)
#             session.add(obj)

async def get_async_session_fastapi() -> AsyncSession:
    async with AsyncSession(engine_async) as conn:
        yield conn

def get_sync_session_fastapi() -> Session:
    with Session(engine_sync) as conn:
        yield conn
