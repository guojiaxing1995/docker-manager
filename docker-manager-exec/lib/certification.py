""" 
@Time    : 2019/11/3 17:58
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : certification.py
@Desc    :
"""
import os

import yaml


def get_certification(host):
    # 获取当前目录
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    with open(parent_dir + '/config/hosts.yaml', 'r') as f:
        yaml_data = yaml.load(f)
    hosts = yaml_data.get('hosts')
    for h in hosts:
        if h['host'] == host:
            return h['certification']

def cert_file_path(host):
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    cert_pem = parent_dir + '/config/certification/' + host + '/cert.pem'
    key_pem = parent_dir + '/config/certification/' + host + '/key.pem'

    return cert_pem,key_pem