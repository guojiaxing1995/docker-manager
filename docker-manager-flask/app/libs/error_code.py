""" 
@Time    : 2018/7/18 19:21
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : error_code.py
@Desc    :
"""

from app.libs.error import APIException

class Success(APIException):
    code = 201
    msg = 'ok'
    error_code = 0

class DeleteSuccess(Success):
    code = 202
    error_code = 1
    msg = 'delete success'

class ClientTypeError(APIException):
    code = 400
    msg = 'client is invalid'
    error_code = 1006

class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000

class NotFound(APIException):
    code = 404
    msg = 'the resource are not found'
    error_code = 1001

class AuthFailed(APIException):
    code = 401
    msg = 'authorization failed'
    error_code = 1005

class Forbidden(APIException):
    code = 403
    msg = 'forbidden,not in scope'
    error_code = 1004

class ModifyFailed(APIException):
    code = 401
    msg = 'Unequal data'
    error_code = 1009

class RepeatFailed(APIException):
    code = 401
    msg = 'data is exist,cannot repeat'
    error_code = 1010

class CaseIsDepend(APIException):
    code = 401
    msg = 'Use cases are dependent'
    error_code = 1016

class FileTypeError(APIException):
    code = 401
    msg = 'file type is error'
    error_code = 1017

class DateNullError(APIException):
    code = 401
    msg = 'data is not null'
    error_code = 1018