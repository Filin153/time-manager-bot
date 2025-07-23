import ics

from schemas import UserActionDTOSchema
import os

import logging

class ToCalendar:
    BASE_USER_ICS_DIR = "./user_ics"

    def __init__(self):
        os.makedirs(self.BASE_USER_ICS_DIR, exist_ok=True)
        self._user_file_path = None
        self._user_tg_id = None

    @property
    def user_tg_id(self):
        return self._user_tg_id
    
    @user_tg_id.setter
    def user_tg_id(self, value: int):
        user_file_path = f"{self.BASE_USER_ICS_DIR}/{value}.ics"
        if f"{value}.ics" not in os.listdir(self.BASE_USER_ICS_DIR):
            with open(user_file_path, "w") as f:
                pass
        
        self._user_file_path = user_file_path
        self._user_tg_id = value

    
    async def update_user_ics(self, event_from_db: UserActionDTOSchema):
        self.user_tg_id = event_from_db.user_tg_id
        try:
            with open(self._user_file_path, "r") as f:
                calendar = ics.Calendar(f.read())
        except Exception as e:
            logging.error(e)
            calendar = ics.Calendar()

        e = ics.Event()
        e.begin = event_from_db.create_at
        e.name = event_from_db.action
        e.end = event_from_db.update_at

        calendar.events.add(e)


        with open(self._user_file_path, 'w') as f:
            f.writelines(calendar.serialize_iter())


        


