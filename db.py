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
    # 根据传入的命令行参数执行对应的操作
    # 例如: python db.py update
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == 'update':
            upgrade_db()
        elif sys.argv[1] == 'new_migration':
            new_migration(sys.argv[2])

