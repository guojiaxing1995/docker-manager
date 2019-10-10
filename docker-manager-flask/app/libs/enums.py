""" 
@Time    : 2018/7/17 19:32
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : enums.py
@Desc    :
"""
from enum import Enum


class ClientTypeEnum(Enum):
    USER_EMAIL = 100
    USER_MOBILE = 101
    #微信小程序
    USER_MINA = 200
    #微信公众号
    USER_WX = 201