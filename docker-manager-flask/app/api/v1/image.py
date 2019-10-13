import math

from docker.errors import APIError, ImageNotFound
from flask import jsonify, current_app

from app.libs.error_code import Success, ImageUsed, DeleteSuccess
from app.libs.error_code import ImageNotFound as NotFound
from app.libs.redprint import Redprint
import docker

from app.validators.client_forms import ClientForm, ImageForm, ListForm

api = Redprint('image')

@api.route('/list',methods=['GET'])
def list():
    form = ListForm().validate_for_api()
    host = form.host.data
    page = int(form.page.data)
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
            image_item['created'] = i.attrs['Created'].split('.')[0]
            if i.attrs['Size']/1000000 > 1:
                image_item['size'] = str(round(i.attrs['Size']/1000000)) + 'MB'
            else:
                image_item['size'] = str(round(i.attrs['Size'] / 1000)) + 'KB'
            image_item['DockerVersion'] = i.attrs['DockerVersion']
            image_list.append(image_item)

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