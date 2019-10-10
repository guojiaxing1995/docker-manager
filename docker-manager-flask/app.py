""" 
@Time    : 2018/7/23 19:34
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : app.py
@Desc    : 入口文件
"""
from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.error import APIException

app = create_app()

@app.errorhandler(Exception)
def framework_error(e):
    app.logger.info(e)
    if isinstance(e,APIException):
        return e
    if isinstance(e,HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(code,msg,error_code)
    else:
        if not app.config['DEBUG']:
            return APIException()
        else:
            raise e



if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'],host=app.config['HOST'],port=app.config['PORT'],threaded=app.config['THREADED'])