""" 
@Time    : 2019/11/5 16:16
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : exec.py
@Desc    :
"""
import threading
import time
from _socket import timeout

import docker
from flask import Flask
from flask_sockets import Sockets
from lib.certification import get_certification, cert_file_path

app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/echo')
def exec(ws):
    host_name = ws.receive()
    host = host_name.split(',')[0]
    name = host_name.split(',')[1]
    certification = get_certification(host)
    # 判断是否鉴权
    if certification:
        cert, key = cert_file_path(host)
        tls_config = docker.tls.TLSConfig(client_cert=(cert, key), verify=False)
        client = docker.APIClient(base_url='tcp://' + host + ':2376', tls=tls_config)
    else:
        client = docker.APIClient(base_url='tcp://' + host + ':2375')
    execCommand = [
        "/bin/sh",
        "-c",
        'TERM=xterm-256color; export TERM; [ -x /bin/bash ] && ([ -x /usr/bin/script ] && /usr/bin/script -q -c "/bin/bash" /dev/null || exec /bin/bash) || exec /bin/sh']
    exec_id = client.exec_create(name, execCommand, stdin=True, tty=True)['Id']
    sock = client.exec_start(exec_id, detach=False, tty=True, socket=True)
    # client.exec_resize(exec_id, height=28, width=200)
    terminalThread = DockerStreamThread(ws, sock)
    terminalThread.start()
    beat_thread = BeatWS(ws, client)
    beat_thread.start()

    try:
        while not ws.closed:
            message = ws.receive()
            if message is not None:
                sed_msg = bytes(message, encoding='utf-8')
                if sed_msg != b'__ping__':
                    sock.send(bytes(message, encoding='utf-8'))
    except Exception as err:
        print(err)
        app.logger.debug(err)
    finally:
        ws.close()
        sock.close()
        client.close()


class DockerStreamThread(threading.Thread):
    def __init__(self, ws, terminalStream):
        super(DockerStreamThread, self).__init__()
        self.ws = ws
        self.terminalStream = terminalStream

    def run(self):
        while not self.ws.closed:
            try:
                dockerStreamStdout = self.terminalStream.recv(2048)
                if dockerStreamStdout is not None:
                    self.ws.send(str(dockerStreamStdout, encoding='utf-8'))
                else:
                    print("docker daemon socket is close")
                    self.ws.close()
            except timeout:
                print('Receive from docker timeout.')
                # self.ws.close()
            except Exception as e:
                print("docker daemon socket err: %s" % e)
                self.ws.close()
                break


class BeatWS(threading.Thread):
    def __init__(self, ws, docker_client):
        super(BeatWS, self).__init__()
        self.ws = ws
        self.docker_client = docker_client

    def run(self):
        while not self.ws.closed:
            time.sleep(5)
            self.docker_client.ping()


@app.route('/')
def hello():
    return '遇事不决 可问春风'


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', 5006), app, handler_class=WebSocketHandler)
    print("web server start ... ")
    server.serve_forever()
