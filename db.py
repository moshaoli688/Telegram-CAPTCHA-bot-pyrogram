from configparser import ConfigParser

from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alembic import command
from model import GroupConfig, BlacklistUser

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


def _import_from_csv(file_path, table):
    import csv
    from datetime import datetime
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        with SessionFactory() as session:
            if table == 'group_config':
                obj = []
                for row in reader:
                    if row[1] == "":
                        row[1] = 'kick'
                    if row[2] == "":
                        row[2] = 'kick'
                    if row[4] == "":
                        row[4] = 'recaptcha'
                    if row[5] == "":
                        row[5] = True
                    elif row[5] == "0":
                        row[5] = False
                    else:
                        row[5] = True
                    if row[6] == "":
                        row[6] = False
                    elif row[6] == "0":
                        row[6] = False
                    else:
                        row[6] = True
                    if row[3] == "":
                        row[3] = 180
                    obj.append(GroupConfig(chat_id=row[0], timeout=row[3], challenge_type=row[4].lower(), failed_action=row[1],
                                       timeout_action=row[2], third_party_blacklist=row[6], global_blacklist=row[5]))
            if table == 'blacklist_user':
                obj = []
                for row in reader:
                    if row[2] == "0":
                        continue
                    linux_timestamp = int(row[1])
                    # 将时间戳转换为datetime对象
                    last_attempt = datetime.fromtimestamp(linux_timestamp)
                    obj.append(BlacklistUser(user_id=row[0], last_attempt=last_attempt, attempt_count=row[3]))
            session.add_all(obj)
            session.commit()


if __name__ == '__main__':
    # 根据传入的命令行参数执行对应的操作
    # 例如: python db.py update
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == 'update':
            upgrade_db()
        elif sys.argv[1] == 'new_migration':
            new_migration(sys.argv[2])
        elif sys.argv[1] == 'import':
            _import_from_csv(sys.argv[2], sys.argv[3])
