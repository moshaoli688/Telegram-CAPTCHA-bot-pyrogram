from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser
from alembic.config import Config
from alembic import command
from model import GroupConfig, BlacklistUser, RecaptchaLog

config = ConfigParser()
config.read('config.ini', encoding='utf-8')
db_config = config['db']

engine = create_engine(db_config['conn_str'])
SessionFactory = sessionmaker(bind=engine)


def upgrade_db():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", db_config['conn_str'])
    command.upgrade(alembic_cfg, "head")


def new_migration(message: str):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", db_config['conn_str'])
    command.revision(alembic_cfg, message=message, autogenerate=True)


if __name__ == '__main__':
    new_migration('change user id to BigInteger')
    upgrade_db()
    ...
