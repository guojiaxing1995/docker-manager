""" 
@Time    : 2018/7/23 19:36
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : __init__.py.py
@Desc    :
"""

#注册蓝图
import logging
import os
import time

from flask_apscheduler import APScheduler
from flask_cors import *

from flask_mail import Mail

from app.libs.socketio import socket_io
from app.libs.util import get_date_str
from .app import Flask

mail = Mail()
scheduler = APScheduler()
app = Flask(__name__)

def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(),url_prefix='/v1')

def register_plugin(app):
    from app.models import task, task_case
    from app.models.base import db
    db.init_app(app)
    with app.app_context():
        db.create_all()

#注册定时任务
def register_scheduler(app):
    scheduler.init_app(app)
    with app.app_context():
        scheduler.start()

def register_logger(app):
    log_dict = {
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING
    }
    # 获取当前目录
    current_dir = os.path.dirname(__file__)
    # 获取当前目录的父级目录
    parent_dir = os.path.dirname(current_dir)
    #date_str = get_date_str
    log_file_name = parent_dir +'/log/flask.log'
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(log_dict[app.config['LEVEL']]) if app.config['LEVEL'] else file_handler.setLevel(logging.INFO)
    logging_format = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(filename)s - %(funcName)s [line:%(lineno)d]: %(message)s')
    file_handler.setFormatter(logging_format)
    app.logger.addHandler(file_handler)

def create_app():

    CORS(app, supports_credentials=True)
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')
    register_blueprints(app)
    #register_plugin(app)
    register_scheduler(app)
    register_logger(app)
    mail.init_app(app)


    socket_io.init_app(app,cors_allowed_origins='*')


    return socket_io,app