from pydantic import BaseModel
from datetime import datetime

class UserActionCreateSchema(BaseModel):
    user_tg_id: int
    action: str

class UserActionDTOSchema(BaseModel):
    user_tg_id: int
    action: str

    create_at: datetime
    update_at: datetime