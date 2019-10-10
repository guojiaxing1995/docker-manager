""" 
@Time    : 2018/7/16 19:51
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : __init__.py.py
@Desc    :
"""
from app.api.v1 import client
from flask import Blueprint


def create_blueprint_v1():
    bp_v1 = Blueprint('v1',__name__)

    client.api.register(bp_v1)
    return bp_v1