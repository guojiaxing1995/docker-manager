""" 
@Time    : 2018/7/26 21:02
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : case_forms.py
@Desc    :
"""
from flask_wtf import Form
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, BooleanField,IntegerField,FileField
from wtforms.validators import DataRequired, AnyOf

from app.validators.base import BaseForm


class CaseForm(BaseForm):
    case_name = StringField(validators=[DataRequired(message='不许为空')])
    method = StringField(validators=[DataRequired(message='不许为空')])
    url = StringField(validators=[DataRequired(message='不许为空')])
    header = StringField()
    data = StringField()
    submission = StringField(validators=[AnyOf(['0','1'])])
    expect_result = StringField(default="870c5c5e54f677dcc61a25b842e5047a1028562f22fd7a987649d4872907cd7490499883ae705d22f12481e0d1f581cde6848f4761a1b87a78781204cbd61ba7")

class CaseBatchForm(BaseForm):
    task_id = StringField(validators=[DataRequired(message='不许为空')])

class CaseDetailForm(BaseForm):
    id = IntegerField(validators=[DataRequired(message='不许为空')],default=-1)
    case_id = StringField()

class CaseSearchForm(BaseForm):
    case_name = StringField(default=None)
    method = StringField(default=None)
    url = StringField(default=None)
    task_id = StringField(default=None)
    #1 true 0 false -1 全部
    is_new = IntegerField(default=1)
    page = IntegerField(default=1)
    user_name = StringField(default=None)
    task_name = StringField(default=None)
    # 1 true 0 false -1 全部
    result = IntegerField(default=-1)
    startDate = StringField(default=None)
    endDate = StringField(default=None)
