""" 
@Time    : 2018/8/5 11:41
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : task_forms.py
@Desc    : task相关接口入参校验
"""
import datetime

from wtforms import StringField,BooleanField,IntegerField
from wtforms.validators import DataRequired, length, AnyOf

from app.libs.util import get_date_str
from app.validators.base import BaseForm


class TaskForm(BaseForm):
    name = StringField(validators=[DataRequired(message='不许为空'), length(min=1, max=20)])
    description = StringField(validators=[length(min=0, max=300)])
    request_header = StringField()

class TaskCaseFormBase(BaseForm):
    task_id = StringField(validators=[DataRequired(message='不许为空')])
    case_id = StringField()
    case_name = StringField()
    url = StringField()
    page = IntegerField(default=1)

class DeleteTaskCaseForm(BaseForm):
    case_id = StringField(validators=[DataRequired(message='不许为空')])

class TaskCaseForm(BaseForm):
    case_name = StringField(validators=[DataRequired(message='不许为空'), length(min=1, max=20)])
    is_run = BooleanField(default = True)
    method = StringField(validators=[DataRequired(message='不许为空')])
    url = StringField(validators=[DataRequired(message='不许为空')])
    header = StringField()
    deal_method = StringField(validators=[AnyOf(['0','1','2','3'])])
    dependent_case = StringField()
    need_position = StringField()
    data = StringField()
    submission = StringField(validators=[AnyOf(['0', '1'])])
    expect_result = StringField(default="870c5c5e54f677dcc61a25b842e5047a1028562f22fd7a987649d4872907cd7490499883ae705d22f12481e0d1f581cde6848f4761a1b87a78781204cbd61ba7")
    task_id = StringField(validators=[DataRequired(message='不许为空')])

class UpdateTaskCaseForm(BaseForm):
    case_id = StringField(validators=[DataRequired(message='不许为空')])
    case_name = StringField(validators=[DataRequired(message='不许为空'), length(min=1, max=20)])
    is_run = BooleanField(default=False)
    method = StringField(validators=[DataRequired(message='不许为空')])
    url = StringField(validators=[DataRequired(message='不许为空')])
    header = StringField()
    deal_method = StringField()
    dependent_case = StringField()
    need_position = StringField()
    data = StringField()
    submission = StringField(validators=[AnyOf(['0', '1'])])
    expect_result = StringField(default="870c5c5e54f677dcc61a25b842e5047a1028562f22fd7a987649d4872907cd7490499883ae705d22f12481e0d1f581cde6848f4761a1b87a78781204cbd61ba7")
    task_id = StringField(validators=[DataRequired(message='不许为空')])

class ReportForm(BaseForm):
    task_id = IntegerField(validators=[DataRequired(message='不许为空')])
    report_date = StringField(default=get_date_str)

class SchedulerAddForm(BaseForm):
    task_id = IntegerField(validators=[DataRequired(message='不许为空')])
    day_of_week = StringField()
    hour = IntegerField()
    minute = IntegerField()
    user_id = IntegerField(validators=[DataRequired(message='不许为空')])
    copy_person = StringField()

class SchedulerUpdateForm(BaseForm):
    scheduler_id = StringField(validators=[DataRequired(message='不许为空')])
    day_of_week = StringField()
    hour = IntegerField()
    minute = IntegerField()
    user_id = IntegerField(validators=[DataRequired(message='不许为空')])
    copy_person = StringField()

class SchedulerPauseForm(BaseForm):
    scheduler_id = StringField(validators=[DataRequired(message='不许为空')])

