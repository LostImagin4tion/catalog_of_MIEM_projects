from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """ Instance stores all app settings, mainly environment variables """

    BASE_URL = 'devcabinet.miem.vmnet.top'
    PUBLIC_API = 'public-api'

    DB_PATH: Optional[str]

    class Config:
        env_file = r'C:\Users\user\PycharmProjects\pythonDed\.env'
        env_file_encoding = 'utf-8'

        # uncomment when testing
        # env_prefix = 'TEST_' + env_prefix


settings = Settings()