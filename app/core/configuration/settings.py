import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class DatabaseSettings(BaseSettings):

    DB_NAME: str = os.getenv("database_name")

    class Config:
        env_file = '.env'

db_settings = DatabaseSettings()


class App_settings(BaseSettings):

    TOKEN: str = os.getenv("TOKEN")

    BOT_NAME: str = os.getenv("BOT_NAME")

    class Config:
        env_file = '.env'

app_settings = App_settings()