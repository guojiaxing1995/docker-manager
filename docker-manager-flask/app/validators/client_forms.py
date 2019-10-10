""" 
@Time    : 2018/7/17 19:36
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : client_forms.py
@Desc    :
"""
from wtforms import StringField, IntegerField, Form
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import AuthFailed
from app.models.user import User
from app.validators.base import BaseForm


class ClientForm(BaseForm):
    account = StringField(validators=[DataRequired(message='不许为空'),length(min=5,max=32)])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self,value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client

class UserEmailForm(ClientForm):
    account = StringField(validators=[Email(message='invalidate email')])
    secret = StringField(validators=[DataRequired(),Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')])
    nickname = StringField(validators=[DataRequired(),length(min=2,max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError(message="account has already existed")

    def validate_nickname(self, value):
        if User.query.filter_by(nickname=value.data).first():
            raise ValidationError(message='nickname has already existed')


class ModifyPasswordForm(ClientForm):
    account = StringField(validators=[Email(message='invalidate email')])
    secret = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')])
    newSecret = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')])