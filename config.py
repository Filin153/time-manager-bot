from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8',
                                      extra="ignore")

    # database
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: int
    PG_HOST_ALEMBIC: str
    PG_PORT_ALEMBIC: str
    PG_DB_NAME: str
    PG_SYNC_URL: str = ""
    PG_ASYNC_URL: str = ""
    PG_ALEMBIC: str = ""

    BOT_TOKEN: str
    ALLOW_USER_IDS: str

    LOG_LEVEL: str


def get_settings():
    settings = Settings()

    settings.PG_ASYNC_URL = f"postgresql+asyncpg://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_HOST}:{settings.PG_PORT}/{settings.PG_DB_NAME}"
    settings.PG_SYNC_URL = f"postgresql://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_HOST}:{settings.PG_PORT}/{settings.PG_DB_NAME}"
    settings.PG_ALEMBIC = f"postgresql://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_HOST_ALEMBIC}:{settings.PG_PORT_ALEMBIC}/{settings.PG_DB_NAME}"

    settings.ALLOW_USER_IDS = list(int(user_id) for user_id in settings.ALLOW_USER_IDS.split(",") if user_id != '')

    return settings


settings = get_settings()
print(settings)
