from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BIGINT
from database.database import Base

class UserActionORM(Base):
    __tablename__ = "user_action"
    
    user_tg_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    action: Mapped[str] = mapped_column(nullable=False)
    stop: Mapped[bool] = mapped_column(nullable=False, default=False)

