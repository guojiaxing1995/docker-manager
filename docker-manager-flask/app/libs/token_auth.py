""" 
@Time    : 2018/7/19 20:27
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : token_auth.py
@Desc    :
"""
import datetime
import time
from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_socpe
from app.models.user import User as U

auth = HTTPBasicAuth()
User = namedtuple('User',['uid','ac_type','scope'])

@auth.verify_password
def verify_password(token,password):
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True

def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid',error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired',error_code=1003)
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    login_time = data['login_time']

    #判断token是否是最新的
    user = U.query.filter_by(id=uid).first()
    if login_time == datetime.datetime.fromtimestamp(86400):
        raise AuthFailed(msg='token is invalid',error_code=1002)
    if time.mktime(user.login_time.timetuple()) != login_time:
        raise AuthFailed(msg='token is expired',error_code=1003)
    #判断是否有权限访问
    allow = is_in_socpe(scope,request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid,ac_type,scope)


#生成token令牌
def create_token(**kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=current_app.config['EMAIL_TOKEN_EXPIRATION'])
    token = s.dumps(dict(**kwargs)).decode('utf-8')

    return token

#验证令牌
def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token.encode('utf-8'))
    except BadSignature:
        raise AuthFailed(msg='token is invalid',error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired',error_code=1003)

    return data
