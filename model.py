from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, BigInteger
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import StrEnum

Base = declarative_base()


class ChallengeType(StrEnum):
    recaptcha = "recaptcha"
    math = "math"


class FailedAction(StrEnum):
    ban = "ban"
    kick = "kick"
    mute = "mute"


class RecaptchaLogAction(StrEnum):
    PageVisit = "PageVisit"
    Failed = "Failed"
    Passed = "Passed"


class BlacklistUser(Base):
    __tablename__ = 'blacklist_user'
    user_id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    last_attempt = Column(DateTime, nullable=False, default=datetime.now)
    attempt_count = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "<blacklist(user_id='%s', last_attempt='%s', attempt_count='%s', created_at='%s', updated_at='%s')>" % (
            self.user_id, self.last_attempt, self.attempt_count, self.created_at, self.updated_at)


class GroupConfig(Base):
    __tablename__ = 'group_config'
    chat_id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    timeout = Column(Integer, nullable=False, default=120)
    challenge_type = Column(String(10), nullable=False, default=ChallengeType.recaptcha)
    failed_action = Column(String(10), nullable=False, default=FailedAction.kick)
    timeout_action = Column(String(10), nullable=False, default=FailedAction.kick)
    third_party_blacklist = Column(Boolean, nullable=False, default=False)
    global_blacklist = Column(Boolean, nullable=False, default=True)

    @validates('challenge_type')
    def validate_challenge_type(self, key, challenge_type):
        if challenge_type not in (m.value for m in ChallengeType):
            raise ValueError(f"Invalid challenge type value: {challenge_type}")
        return challenge_type

    @validates('failed_action')
    def validate_failed_action(self, key, failed_action):
        if failed_action not in (m.value for m in FailedAction):
            raise ValueError(f"Invalid failed action value: {failed_action}")
        return failed_action

    @validates('timeout_action')
    def validate_timeout_action(self, key, timeout_action):
        if timeout_action not in (m.value for m in FailedAction):
            raise ValueError(f"Invalid timeout action value: {timeout_action}")
        return timeout_action

    @validates('third_party_blacklist')
    def validate_third_party_blacklist(self, key, third_party_blacklist):
        if not isinstance(third_party_blacklist, bool):
            raise ValueError(f"Invalid third party blacklist value: {third_party_blacklist}")
        return third_party_blacklist

    @validates('global_blacklist')
    def validate_global_blacklist(self, key, global_blacklist):
        if not isinstance(global_blacklist, bool):
            raise ValueError(f"Invalid global blacklist value: {global_blacklist}")
        return global_blacklist

    def __repr__(self):
        return "<group_config(group_id='%s', timeout='%s', challenge_type='%s', failed_action='%s', timeout_action='%s', third_party_blacklist='%s', global_blacklist='%s')>" % (
            self.chat_id, self.timeout, self.challenge_type, self.failed_action, self.timeout_action,
            self.third_party_blacklist, self.global_blacklist)


class RecaptchaLog(Base):
    __tablename__ = 'recaptcha_log'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    group_id = Column(BigInteger, ForeignKey('group_config.chat_id'), nullable=False)
    user_id = Column(BigInteger, nullable=False)
    challenge_id = Column(String(64), nullable=False)
    ip_addr = Column(String(64), nullable=False)
    user_agent = Column(Text, nullable=False)
    action = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "<recaptcha_log(id='%s', group_id='%s', user_id='%s', challenge_id='%s', ip_addr='%s', user_agent='%s', action='%s', created_at='%s', updated_at='%s')>" % (
            self.id, self.group_id, self.user_id, self.challenge_id, self.ip_addr, self.user_agent, self.action,
            self.created_at, self.updated_at)

    def __str__(self):
        return f"IP地址: `{self.ip_addr}`\nUA：`{self.user_agent}`\n状态：`{self.action}`\n时间：`{self.created_at}`\n"
