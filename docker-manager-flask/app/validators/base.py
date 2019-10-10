""" 
@Time    : 2018/7/18 20:37
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : base.py
@Desc    :
"""
from flask import request
from wtforms import Form

from app.libs.error_code import ParameterException


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm,self).__init__(data=data,**args)

    def validate_for_api(self):
        valid = super(BaseForm,self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)
        return self
