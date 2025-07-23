from fastapi import FastAPI
from fastapi.responses import FileResponse
from utils.to_ics import ToCalendar
import uvicorn

app = FastAPI(
    docs_url=None,
    redoc_url=None,
)

@app.get("/time-manager/ics/{user_id}")
async def get_user_ics_file(user_id: int):
    to_ical = ToCalendar()
    file_path = to_ical.get_user_ics_path(user_id=user_id)
    return FileResponse(
        path=file_path,
        headers={
            "Content-type": "text/calendar"
        },
        filename=f"time_manager_{user_id}.ics",
    )

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port="8080")

