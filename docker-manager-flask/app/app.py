""" 
@Time    : 2018/7/23 19:36
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : app.py
@Desc    :
"""
from datetime import date

from flask import Flask as _Flask

from flask.json import JSONEncoder as _JSONEncoder

from app.libs.error import APIException


class JSONEncoder(_JSONEncoder):
    def default(self,o):
        if hasattr(o,'keys') and hasattr(o,'__getitem__'):
            return dict(o)
        if isinstance(o,date):
            return o.strftime('%Y-%m-%d')
        raise APIException()

class Flask(_Flask):
    json_encoder = JSONEncoder