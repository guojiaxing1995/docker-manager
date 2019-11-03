import math
import time

import docker
from flask import jsonify, current_app
from flask_socketio import emit

from app import socket_io
from app.libs.certification import get_certification, cert_file_path
from app.libs.error_code import Success, StopFail, StartFail, RemoveFail
from app.validators.client_forms import ListForm, ContainerForm
from app.libs.redprint import Redprint

api = Redprint('container')

@api.route('/list',methods=['GET'])
def list():
    form = ListForm().validate_for_api()
    host = form.host.data
    page = int(form.page.data)
    search = form.search.data
    certification = get_certification(host)
    # 判断是否鉴权
    if certification:
        cert,key = cert_file_path(host)
        tls_config = docker.tls.TLSConfig(client_cert=(cert, key),verify=False)
        client = docker.DockerClient(base_url='tcp://' + host + ':2376', tls=tls_config)
    else:
        client = docker.DockerClient(base_url='tcp://' + host + ':2375')
    container_list = client.containers.list(all=True)

    containers= []
    for c in container_list:
        container = {}
        container['name'] = c.name
        container['id'] = c.short_id
        container['status'] = c.status
        container['ports'] = str(c.ports).replace('{','').replace('}','').replace(': None','').replace("'HostIp': ",'').replace(", 'HostPort'",'')
        container['created'] = c.attrs['Created'].split('.')[0].replace('T',' ')
        container['restartCount'] = c.attrs['RestartCount']
        container['cmd'] = str(c.attrs['Config']['Cmd'])
        container['image'] = c.attrs['Config']['Image']
        if c.attrs['HostConfig']['Binds']:
            container['volumes'] = str(c.attrs['HostConfig']['Binds']).replace(':rw', '')
        else:
            container['volumes'] = ''
        container['network'] = c.attrs['HostConfig']['NetworkMode']
        #container['portsSet'] = str(c.attrs['HostConfig']['PortBindings']).replace('{', '').replace('}', '').replace("'HostIp': '', 'HostPort': ", '')
        containers.append(container)

    #查询
    if search:
        container_list_new = []
        for c in containers:
            if search in c['name'] or search in c['id']:
                container_list_new.append(c)
        containers = container_list_new

    #分页
    PAGE_NUM = current_app.config['PAGE_NUM']
    start = (page - 1) * PAGE_NUM
    end = page * PAGE_NUM
    data = containers[start:end]
    paginate_result = {
        'data': data,
        'page': page,
        'pages': math.ceil(len(containers)/PAGE_NUM),
        'total': len(containers)
    }

    client.close()

    return jsonify(paginate_result)

@api.route('/stop',methods=['GET'])
def stop():
    form = ContainerForm().validate_for_api()
    host = form.host.data
    name_or_Id = form.nameOrId.data
    certification = get_certification(host)
    # 判断是否鉴权
    if certification:
        cert,key = cert_file_path(host)
        tls_config = docker.tls.TLSConfig(client_cert=(cert, key),verify=False)
        client = docker.DockerClient(base_url='tcp://' + host + ':2376', tls=tls_config)
    else:
        client = docker.DockerClient(base_url='tcp://' + host + ':2375')
    try:
        c = client.containers.get(name_or_Id)
        c.stop()
    except Exception:
        client.close()
        return StopFail()

    client.close()
    return Success(msg='容器停止成功')

@api.route('/start',methods=['GET'])
def start():
    form = ContainerForm().validate_for_api()
    host = form.host.data
    name_or_Id = form.nameOrId.data
    certification = get_certification(host)
    # 判断是否鉴权
    if certification:
        cert,key = cert_file_path(host)
        tls_config = docker.tls.TLSConfig(client_cert=(cert, key),verify=False)
        client = docker.DockerClient(base_url='tcp://' + host + ':2376', tls=tls_config)
    else:
        client = docker.DockerClient(base_url='tcp://' + host + ':2375')
    try:
        c = client.containers.get(name_or_Id)
        c.start()
    except Exception:
        client.close()
        return StartFail()

    client.close()
    return Success(msg='容器启动成功')

@api.route('/remove',methods=['GET'])
def remove():
    form = ContainerForm().validate_for_api()
    host = form.host.data
    name_or_Id = form.nameOrId.data
    volume = form.volume.data
    certification = get_certification(host)
    # 判断是否鉴权
    if certification:
        cert,key = cert_file_path(host)
        tls_config = docker.tls.TLSConfig(client_cert=(cert, key),verify=False)
        client = docker.DockerClient(base_url='tcp://' + host + ':2376', tls=tls_config)
    else:
        client = docker.DockerClient(base_url='tcp://' + host + ':2375')
    try:
        c = client.containers.get(name_or_Id)
        c.remove(v=volume)
    except Exception:
        client.close()
        return RemoveFail()

    client.close()
    return Success(msg='容器删除成功')


@socket_io.on('logs')
def logs(data):
    host = data.get('host')
    name = data.get('name')
    certification = get_certification(host)
    # 判断是否鉴权
    if certification:
        cert,key = cert_file_path(host)
        tls_config = docker.tls.TLSConfig(client_cert=(cert, key),verify=False)
        client = docker.DockerClient(base_url='tcp://' + host + ':2376', tls=tls_config)
    else:
        client = docker.DockerClient(base_url='tcp://' + host + ':2375')
    c = client.containers.get(name)
    for line in c.logs(stream=True, tail=20, follow=True):
        print(line.decode('utf-8').strip())
        emit(host + name, {'name': name, 'msg': line.decode('utf-8').strip()})


@api.route('/shell')
def shell():
    form = ContainerForm().validate_for_api()
    host = 'www.guojiaxing.red'
    name_or_Id = 'f5ca53929c1d'
    certification = get_certification(host)
    # 判断是否鉴权
    if certification:
        cert,key = cert_file_path(host)
        tls_config = docker.tls.TLSConfig(client_cert=(cert, key),verify=False)
        client = docker.DockerClient(base_url='tcp://' + host + ':2376', tls=tls_config)
    else:
        client = docker.DockerClient(base_url='tcp://' + host + ':2375')
    c = client.containers.get(name_or_Id)
    client.close()
    # a = c.exec_run(['touch', 'a'],stream=True,stdin=True,tty=True)
    for line in c.exec_run(['/bin/sh','touch', 'bbb'],stream=True,stdin=True,tty=True).output:
        return line


@socket_io.on_error()        # Handles the default namespace
def error_handler(e):
    raise RuntimeError()

@socket_io.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socket_io.on('disconnect')
def test_disconnect():
    print('Client disconnected')

