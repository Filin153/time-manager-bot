import os
import shutil
import pytest
from utils.to_ics import ToCalendar  # Импортируйте путь к вашему классу правильно

# Пример mock-схемы UserActionDTOSchema
class MockUserActionDTOSchema:
    def __init__(self, user_tg_id, create_at, update_at, action):
        self.user_tg_id = user_tg_id
        self.create_at = create_at
        self.update_at = update_at
        self.action = action

@pytest.fixture
def temp_ics_dir():
    test_dir = "./user_ics"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    yield test_dir
    shutil.rmtree(test_dir)

@pytest.mark.asyncio
async def test_create_and_update_ics(temp_ics_dir):
    from datetime import datetime, timedelta

    user_id = 12345
    calendar = ToCalendar()

    # Создаем моковое событие
    now = datetime.utcnow()
    event = MockUserActionDTOSchema(
        user_tg_id=user_id,
        create_at=now,
        update_at=now + timedelta(hours=1),
        action="Test Event"
    )

    # Добавляем событие в календарь
    await calendar.update_user_ics(event)

    # Убедимся, что файл создался
    expected_path = f"{temp_ics_dir}/{user_id}.ics"
    assert os.path.exists(expected_path)

    # Проверяем содержимое файла
    with open(expected_path, "r") as f:
        content = f.read()
        assert "BEGIN:VEVENT" in content
        assert "Test Event" in content
