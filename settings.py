from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Database:
    async_db_url: str
    db_url: str
    db_echo: bool


@dataclass
class S3:
    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str


@dataclass
class Settings:
    bots: Bots
    db: Database
    s3: S3


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str('BOT_TOKEN'),
            admin_id=env.int('ADMIN_ID')
        ),
        db=Database(
            async_db_url=env.str('DATABASE_URL_ASYNC'),
            db_url=env.str('DATABASE_URL'),
            db_echo=env.bool('DB_ECHO')
        ),
        s3=S3(
            access_key=env.str('ACCESS_KEY'),
            secret_key=env.str('SECRET_KEY'),
            endpoint_url=env.str('ENDPOINT_URL'),
            bucket_name=env.str('BUCKET_NAME'),
        )
    )


settings = get_settings('.env')