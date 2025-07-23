from pydantic import BaseModel

class UserActionCreateSchema(BaseModel):
    user_tg_id: int
    action: str

class UserActionDTOSchema(BaseModel):
    user_tg_id: int
    action: str

    create_at: str
    update_at: str