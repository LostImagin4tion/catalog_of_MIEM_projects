from pydantic import BaseSettings


class Settings(BaseSettings):
    """ Instance stores all app settings, mainly environment variables """

    BASE_URL = 'https://devcabinet.miem.vmnet.top'
    PUBLIC_API = 'public-api'

    DB_PATH = 'mysql+pymysql://root:admin@localhost/pythonProject?charset=utf8mb4'


settings = Settings()
