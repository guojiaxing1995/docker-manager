import json
import math

from docker.errors import APIError, ImageNotFound
from flask import jsonify, current_app

from app.libs.error_code import Success, ImageUsed, DeleteSuccess, DockerRunFail, PullFail
from app.libs.error_code import ImageNotFound as NotFound
from app.libs.redprint import Redprint
import docker

from app.validators.client_forms import ClientForm, ImageForm, ListForm, PullForm

api = Redprint('image')

@api.route('/list',methods=['GET'])
def list():
    form = ListForm().validate_for_api()
    host = form.host.data
    page = int(form.page.data)
    search = form.search.data
    client = docker.DockerClient(base_url='tcp://' + host + ':2375')
    images = client.images.list()
    image_list = []
    for i in images:
        for image_tag in i.attrs['RepoTags']:
            image_item = {}
            image_name = image_tag.split(':')[0]
            image_tag = image_tag.split(':')[1]
            image_item['name'] = image_name
            image_item['tag'] = image_tag
            image_item['id'] = i.short_id.split(':')[1]
            image_item['created'] = i.attrs['Created'].split('.')[0].replace('T',' ')
            if i.attrs['Size']/1000000 > 1:
                image_item['size'] = str(round(i.attrs['Size']/1000000)) + 'MB'
            else:
                image_item['size'] = str(round(i.attrs['Size'] / 1000)) + 'KB'
            image_item['DockerVersion'] = i.attrs['DockerVersion']
            image_list.append(image_item)
    #查询
    if search:
        image_list_new = []
        for i in image_list:
            if search in i['name'] or search in i['id']:
                image_list_new.append(i)
        image_list = image_list_new
    PAGE_NUM = current_app.config['PAGE_NUM']
    start = (page - 1) * PAGE_NUM
    end = page * PAGE_NUM
    data = image_list[start:end]
    paginate_result = {
        'data': data,
        'page': page,
        'pages': math.ceil(len(image_list)/PAGE_NUM),
        'total': len(image_list)
    }
    client.close()
    return jsonify(paginate_result)

@api.route('/delete',methods=['GET'])
def delete():
    form = ImageForm().validate_for_api()
    host = form.host.data
    image = form.image.data
    client = docker.DockerClient(base_url='tcp://' + host + ':2375')
    try:
        client.images.remove(image)
    except ImageNotFound:
        client.close()
        return NotFound()
    except APIError:
        client.close()
        return ImageUsed()
    # client.images.remove(image)
    client.close()

    return DeleteSuccess(msg='镜像删除成功')

@api.route('/run',methods=['POST'])
def run():
    form = ImageForm().validate_for_api()
    host = form.host.data
    image = form.image.data
    command = form.command.data
    name = form.name.data
    restart = form.restart.data
    links = form.links.data
    ports = form.ports.data
    volumes = form.volumes.data
    if links:
        links_dick = {}
        for link in links.split(','):
            links_dick[link.split(':')[0]] = link.split(':')[1]
        links = links_dick
    else:
        links = None

    if ports:
        ports_dick = {}
        for port in ports.split(','):
            ports_dick[port.split(':')[1]] = port.split(':')[0]
        ports = ports_dick
    else:
        ports = None

    if volumes:
        volumes_dick = {}
        for volume in volumes.split(','):
            volumes_dick[volume.split(':')[0]] = {'bind': volume.split(':')[1], 'mode': 'rw'}
        volumes = volumes_dick
    else:
        volumes = None

    if restart:
        restart_policy = {"Name": "always"}
    else:
        restart_policy = None

    client = docker.DockerClient(base_url='tcp://' + host + ':2375')
    try:
        container = client.containers.run(image, command, detach=True, name=name, links=links, ports=ports,
                                          restart_policy=restart_policy, volumes=volumes)
        id = container.short_id
        name = container.attrs['Name'][1:]
        container = {
            "id": id,
            "name": name
        }
        client.close()
        return jsonify(container)
    except Exception:
        client.close()
        return DockerRunFail()

@api.route('/search',methods=['GET'])
def search():
    form = ImageForm().validate_for_api()
    host = form.host.data
    image = form.image.data
    client = docker.DockerClient(base_url='tcp://' + host + ':2375')
    images = client.images.search(image)
    for i in images:
        i['tag'] = ''
    client.close()
    return jsonify(images)

@api.route('/pull',methods=['GET'])
def pull():
    form = PullForm().validate_for_api()
    host = form.host.data
    image = form.image.data
    tag = form.tag.data
    client = docker.DockerClient(base_url='tcp://' + host + ':2375')
    if not tag:
        tag = None
    try:
        client.images.pull(image,tag)
    except Exception:
        client.close()
        return PullFail()
    client.close()
    return Success(msg='镜像拉取成功')
