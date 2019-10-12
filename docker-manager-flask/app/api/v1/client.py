""" 
@Time    : 2018/7/17 19:28
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : client.py
@Desc    :
"""
import os

import yaml
from flask import jsonify

from app.libs.error_code import Success
from app.libs.redprint import Redprint
import docker

from app.validators.client_forms import ClientForm

api = Redprint('client')

@api.route('/info',methods=['GET'])
def create_client():
    form = ClientForm().validate_for_api()
    host = form.host.data
    client = docker.DockerClient(base_url='tcp://' + host + ':2375')
    info_all = client.info()
    info = {}
    info['Name'] = info_all['Name']
    info['OperatingSystem'] = info_all['OperatingSystem']
    info['DockerRootDir'] = info_all['DockerRootDir']
    info['NCPU'] = info_all['NCPU']
    info['MemTotal'] = round(info_all['MemTotal']/1024/1024/1024, 2)
    info['ServerVersion'] = info_all['ServerVersion']
    info['Containers'] = info_all['Containers']
    info['ContainersRunning'] = info_all['ContainersRunning']
    info['ContainersStopped'] = info_all['ContainersStopped']
    info['Images'] = info_all['Images']
    client.close()
    return jsonify(info)

@api.route('/imageList',methods=['GET'])
def image_list():
    form = ClientForm().validate_for_api()
    host = form.host.data
    client = docker.DockerClient(base_url='tcp://' + host + ':2375')
    images = client.images.list()
    image_list = []
    for image in images:
        image_list += image.attrs['RepoTags']
    client.close()
    return jsonify(image_list)

@api.route('/containerList',methods=['GET'])
def container_list():
    form = ClientForm().validate_for_api()
    host = form.host.data
    client = docker.DockerClient(base_url='tcp://' + host + ':2375')
    containers = client.containers.list(all)
    container_list = {
        'running_list': [],
        'exited_list': [],
        'all_list': []
    }
    for container in containers:
        container_list['all_list'].append(container.attrs['Name'][1:])
        if container.attrs['State']['Status'] == 'running':
            container_list['running_list'].append(container.attrs['Name'][1:])
        if container.attrs['State']['Status'] == 'exited':
            container_list['exited_list'].append(container.attrs['Name'][1:])
    client.close()
    return jsonify(container_list)

@api.route('/hosts',methods=['GET'])
def hosts():
    # 获取当前目录
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    parent_parent_dir = os.path.dirname(parent_dir)
    with open(parent_parent_dir + '/config/hosts.yaml', 'r') as f:
        yaml_data = yaml.load(f)
    hosts = yaml_data.get('hosts')
    hostList = []
    for host in hosts:
        hostList.append({'value': host, 'label': host})
    return jsonify(hostList)