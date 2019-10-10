""" 
@Time    : 2018/7/17 19:28
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : client.py
@Desc    :
"""
from flask import jsonify

from app.libs.error_code import Success
from app.libs.redprint import Redprint
import docker

api = Redprint('client')

@api.route('/info',methods=['GET'])
def create_client():
    client = docker.DockerClient(base_url='tcp://www.guojiaxing.red:2375')
    info = client.info()
    return jsonify(info)

