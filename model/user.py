#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 19-2-20

import datetime
from enum import Enum
from hashlib import md5

from mongoengine import *

_MD5_SALT = 'a random string'  # 盐一旦使用后不可更改，否则历史数据会无效


class Roles(Enum):
    Admin = 'admin'
    Default = 'user'


class UserModel(Document):
    # email = EmailField(max_length=128, required=True, unique=True)  # todo: enable
    # password = StringField(max_length=128, required=True)  # todo: enable
    email = EmailField(max_length=128)
    phone = StringField(max_length=16)
    __password = StringField(max_length=255, db_field='password')
    name = StringField(max_length=32, required=True)
    __role = StringField(max_length=32, default=Roles.Default.value)
    register_time = DateTimeField(default=lambda: datetime.datetime.utcnow())
    last_login_time = DateTimeField(default=lambda: datetime.datetime.utcnow())
    questions_history = DictField(default={})  # {question_id: fetched_datetime, ...}
    questions_liked = DictField(default={})  # {question_id: liked_datetime, ...}
    users_similar = DictField(default={})  # {user_id: similarity, ...}
    # student_id = StringField(max_length=32)  # student_id should be unique. todo: remove? should remove
    # university = StringField(max_length=32) # 改成枚举
    # college = StringField(max_length=32)
    # occupation = StringField(max_length=32) # 改成枚举
    # birthday = DateTimeField()
    # gender = StringField(max_length=8)
    wx_id = StringField(max_length=64, default='')
    vip_start_time = DateTimeField(default=lambda: datetime.datetime.utcnow())
    vip_end_time = DateTimeField(default=lambda: datetime.datetime.utcnow() + datetime.timedelta(days=1))
    remaining_exam_num = IntField(min_value=0, default=3)
    invitation_code = StringField(max_length=64, default='')

    meta = {'collection': 'users', 'strict': False}

    @property
    def role(self):
        return Roles(self.__role)

    @role.setter
    def role(self, Role):
        if isinstance(Role, Roles):
            self.__role = Role.value
        else:
            raise TypeError('Role must be a member of class Roles')

    def __repr__(self):
        return "{id:%s, email:%s, name:%s, role:%s}" % (self.id, self.email, self.name, self.role)

    def __str__(self):
        return "{id:%s,name:%s,register_time:%s,last_login_time:%s}" % (
            self.id, self.name.__str__(), self.register_time.__str__(), self.last_login_time.__str__())

    def is_admin(self):
        return self.__role == Roles.Admin.value

    def check_password(self, password: str):
        """验证密码（前后空格将被忽略）

        Args:
            password: 明文密码

        Returns:
            验证结果，True|False (bool)
        """
        password = password.strip()
        hash_obj = md5()
        hash_obj.update((password + _MD5_SALT).encode())
        return self.__password == hash_obj.hexdigest()

    def set_password(self, password: str):
        """设置hash后的密码但不保存，不要忘记手动保存！（前后空格将被忽略）

        Args:
            password: 明文密码

        Returns:
            None
        """
        password = password.strip()
        hash_obj = md5()
        hash_obj.update((password + _MD5_SALT).encode())
        self.__password = hash_obj.hexdigest()
