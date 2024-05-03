import datetime
import logging

from db import SessionFactory
from model import GroupConfig, BlacklistUser, RecaptchaLog


def get_user(user_id):
    with SessionFactory() as session:
        user = session.query(BlacklistUser).filter_by(user_id=user_id).first()
        if user is None:
            return None
        else:
            return user


def get_user_status(user_id):
    with SessionFactory() as session:
        user = session.query(BlacklistUser).filter_by(user_id=user_id).first()
        if user is None:
            return 0
        else:
            return 1
    # stmt = "SELECT blacklist FROM user WHERE user_id == (?)"
    # cur = self.conn.cursor()
    # try:
    #     cur.execute(stmt, (user_id,))
    #     result = cur.fetchone()
    # except sqlite3.Error as e:
    #     logging.error(str(e))
    #     return None
    # if result is None:
    #     return 0
    # else:
    #     return result[0]


def update_last_try(time, user_id):
    with SessionFactory() as session:
        user = session.query(BlacklistUser).filter_by(user_id=user_id).first()
        if user is None:
            logging.error('User not found')
        else:
            user.last_attempt = time
            session.commit()
    # stmt = "UPDATE user SET last_try = (?) WHERE user_id == (?)"
    # cur = self.conn.cursor()
    # try:
    #     cur.execute(stmt, (time, user_id,))
    #     self.conn.commit()
    # except sqlite3.Error as e:
    #     logging.error(str(e))


def try_count_plus_one(user_id):
    with SessionFactory() as session:
        user = session.query(BlacklistUser).filter_by(user_id=user_id).first()
        if user is None:
            logging.error('User not found')
        else:
            user.attempt_count += 1
            session.commit()
    # stmt = "UPDATE user SET try_count = try_count + 1 WHERE user_id == (?)"
    # cur = self.conn.cursor()
    # try:
    #     cur.execute(stmt, (user_id,))
    #     self.conn.commit()
    # except sqlite3.Error as e:
    #     logging.error(str(e))


def new_blacklist(time, user_id):
    # tested
    with SessionFactory() as session:
        user = BlacklistUser(user_id=user_id, last_attempt=time)
        session.add(user)
        session.commit()
    # stmt = "INSERT OR REPLACE INTO user (last_try, user_id) VALUES (?,?)"
    # try:
    #     self.conn.execute(stmt, (time, user_id,))
    #     self.conn.commit()
    # except sqlite3.Error as e:
    #     logging.error(str(e))


# def blacklist(self, user_id):
#     stmt = "UPDATE user SET blacklist = 1 where user_id == (?)"
#     args = user_id
#     try:
#         self.conn.execute(stmt, (args,))
#         self.conn.commit()
#     except sqlite3.Error as e:
#         logging.error(str(e))


# def whitelist(self, user_id):
#     with SessionFactory() as session:
#         user = session.query(BlacklistUser).filter_by(user_id=user_id).first()
#         if user is None:
#             logging.error('User not found')
#         else:
#             session.delete(user)
#             session.commit()
#     # stmt = "UPDATE user SET blacklist = 0 where user_id == (?)"
#     # args = user_id
#     # try:
#     #     self.conn.execute(stmt, (args,))
#     #     self.conn.commit()
#     # except sqlite3.Error as e:
#     #     logging.error(str(e))


def get_try_count(user_id):
    with SessionFactory() as session:
        user = session.query(BlacklistUser).filter_by(user_id=user_id).first()
        if user is None:
            return 0
        else:
            return user.attempt_count
    # stmt = "SELECT try_count FROM user WHERE user_id == (?)"
    # cur = self.conn.cursor()
    # try:
    #     cur.execute(stmt, (user_id,))
    #     result = cur.fetchone()
    # except sqlite3.Error as e:
    #     logging.error(str(e))
    #     return None
    # if result is None:
    #     return 0
    # else:
    #     return result[0]


def get_all_user_ids():
    with SessionFactory() as session:
        user = session.query(BlacklistUser).all()
        if user is None:
            return 0
        else:
            return [i.user_id for i in user]
    # stmt = "SELECT user_id FROM user"
    # cur = self.conn.cursor()
    # try:
    #     cur.execute(stmt)
    #     result = [i[0] for i in cur.fetchall()]
    #     # cur.fetchall() 是返回一个 tuples，只能用这个方法了转成 list 处理了，如果有更好的方法麻烦告诉我
    # except sqlite3.Error as e:
    #     logging.error(str(e))
    #     return None
    # if result is None:
    #     return 0
    # else:
    #     return result


def delete_user(user_id):
    with SessionFactory() as session:
        user = session.query(BlacklistUser).filter_by(user_id=user_id).first()
        if user is None:
            logging.error('User not found')
        else:
            session.delete(user)
            session.commit()
    # stmt = "DELETE FROM user WHERE user_id = (?)"
    # args = user_id
    # try:
    #     self.conn.executemany(stmt, args)
    #     self.conn.commit()
    # except sqlite3.Error as e:
    #     logging.error(str(e))


def get_group_config(group_id, field: str = 'all'):
    with SessionFactory() as session:
        group = session.query(GroupConfig).filter_by(chat_id=group_id).first()
        if group is None:
            return None
        else:
            if field == 'challenge_failed_action':
                return group.failed_action
            elif field == 'challenge_timeout_action':
                return group.timeout_action
            elif field == 'challenge_timeout':
                return group.timeout
            elif field == 'challenge_type':
                return group.challenge_type
            elif field == 'enable_global_blacklist':
                return group.global_blacklist
            elif field == 'enable_third_party_blacklist':
                return group.third_party_blacklist
            elif field == 'all':
                return {'challenge_failed_action': group.failed_action,
                        'challenge_timeout_action': group.timeout_action,
                        'challenge_timeout': group.timeout, 'challenge_type': group.challenge_type,
                        'enable_global_blacklist': group.global_blacklist,
                        'enable_third_party_blacklist': group.third_party_blacklist}
            else:
                return None
    # """
    # 获取群配置，默认返回所有配置，可以指定返回某个配置
    # field: 值为 challenge_failed_action,
    # challenge_timeout_action,
    # challenge_timeout,
    # challenge_type,
    # enable_global_blacklist,
    # enable_third_party_blacklist
    #
    # return: 如果指定了 field，返回指定的配置，否则返回所有配置
    #
    # """
    #
    # stmt = "SELECT * FROM group_config WHERE group_id == (?)"
    # args = group_id
    # cur = self.conn.cursor()
    # try:
    #     cur.execute(stmt, (args,))
    #     result = cur.fetchone()
    #     if result is None:
    #         return None
    #     elif field == 'challenge_failed_action':
    #         return result[1]
    #     elif field == 'challenge_timeout_action':
    #         return result[2]
    #     elif field == 'challenge_timeout':
    #         return result[3]
    #     elif field == 'challenge_type':
    #         return result[4]
    #     elif field == 'enable_global_blacklist':
    #         return result[5]
    #     elif field == 'enable_third_party_blacklist':
    #         return result[6]
    #     elif field == 'all':
    #         group_config = {'challenge_failed_action': result[1], 'challenge_timeout_action': result[2],
    #                         'challenge_timeout': result[3], 'challenge_type': result[4],
    #                         'enable_global_blacklist': result[5], 'enable_third_party_blacklist': result[6]}
    #         # remove None value
    #         null_key = [i for i in group_config if group_config[i] is None]
    #         for key in null_key:
    #             group_config.pop(key)
    #         return group_config
    #     else:
    #         return None
    # except sqlite3.Error as e:
    #     logging.error(str(e))
    #     return None


def new_group_config(group_id):
    with SessionFactory() as session:
        group = GroupConfig(chat_id=group_id)
        session.add(group)
        session.commit()
    # stmt = "INSERT OR REPLACE INTO group_config (group_id) VALUES (?)"
    # args = (group_id,)
    # try:
    #     self.conn.execute(stmt, args)
    #     self.conn.commit()
    # except sqlite3.Error as e:
    #     logging.error(str(e))
    #     return False


def set_group_config(group_id, key, value):
    # tested 80% passed
    with SessionFactory() as session:
        group = session.query(GroupConfig).filter_by(chat_id=group_id).first()
        if group is None:
            new_group_config(group_id)
        else:
            if key == 'challenge_failed_action':
                group.failed_action = value
            elif key == 'challenge_timeout_action':
                group.timeout_action = value
            elif key == 'challenge_timeout':
                group.timeout = value
            elif key == 'challenge_type':
                group.challenge_type = value
            elif key == 'enable_global_blacklist':
                group.global_blacklist = value
            elif key == 'enable_third_party_blacklist':
                group.third_party_blacklist = value
            else:
                return False
            session.commit()
    return True
    # if self.get_group_config(group_id) is None:
    #     self.new_group_config(group_id)
    #
    # value_type = 'str'
    #
    # if key == 'challenge_failed_action':
    #     if value != 'ban' and value != 'kick':
    #         return False
    #     stmt = "UPDATE group_config SET challenge_failed_action = (?) WHERE group_id = (?)"
    # elif key == 'challenge_timeout_action':
    #     if value != 'ban' and value != 'kick' and value != 'mute':
    #         return False
    #     stmt = "UPDATE group_config SET challenge_timeout_action = (?) WHERE group_id = (?)"
    # elif key == 'challenge_timeout':
    #     stmt = "UPDATE group_config SET challenge_timeout = (?) WHERE group_id = (?)"
    #     value_type = 'int'
    # elif key == 'challenge_type':
    #     if value != 'math' and value != 'reCAPTCHA':
    #         return False
    #     stmt = "UPDATE group_config SET challenge_type = (?) WHERE group_id = (?)"
    # elif key == 'enable_global_blacklist':
    #     stmt = "UPDATE group_config SET enable_global_blacklist = (?) WHERE group_id = (?)"
    #     value_type = 'bool'
    # elif key == 'enable_third_party_blacklist':
    #     stmt = "UPDATE group_config SET enable_third_party_blacklist = (?) WHERE group_id = (?)"
    #     value_type = 'bool'
    # else:
    #     return False
    #
    # if value_type == 'int':
    #     try:
    #         value = int(value)
    #     except ValueError:
    #         return False
    # if value_type == 'bool':
    #     try:
    #         value = int(value)
    #         print(value)
    #         if value != 0 and value != 1:
    #             return False
    #     except ValueError:
    #         return False
    #
    # args = (value, group_id)
    # cur = self.conn.cursor()
    # try:
    #     cur.execute(stmt, args)
    #     rows = cur.rowcount
    #     self.conn.commit()
    #     if rows == 0:
    #         return False
    #     else:
    #         return True
    # except sqlite3.Error as e:
    #     logging.error(str(e))


if __name__ == '__main__':
    ...