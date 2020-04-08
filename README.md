<h1 align="center">docker-manager</h1>
<h4 align="center">docker可视化管理平台</h3>

<p align="center">
  <a href="https://www.python.org/" rel="nofollow"><img src="https://img.shields.io/badge/python-%3D%3D3.6-blue.svg" alt="python version" data-canonical-src="https://img.shields.io/badge/python-%3D%3D3.6-blue.svg" style="max-width:100%;"></a>
  <a href="http://flask.pocoo.org/docs/1.0/" rel="nofollow">
  <img src="https://img.shields.io/badge/flask-%3D%3D1.0.2-yellow.svg" alt="flask version" data-canonical-src="https://img.shields.io/badge/flask-%3D%3D1.0.2-yellow.svg" style="max-width:100%;"></a>
  <a href="https://nodejs.org/en/"><img src="https://img.shields.io/badge/node-%3D%3D10.16.0-green" alt="node version" data-canonical-src="https://img.shields.io/badge/vue-%3D%3D2.9.6-green.svg" style="max-width:100%;"></a>
</p>

### 项目介绍
docker可视化管理平台，使用vue + python flask 前后端分离实现。
<br>
这个工具设计的初衷是为了更加方便的对多台服务器进行docker管理，哪台服务器上有些什么容器和镜像一目了然。减少平时工作中切换登录不同服务器和执行命令的时间，提高工作效率。同时也为不熟悉docker的人提供帮助，能够更加直观的认识和学习docker。
目前实现了工作中一般用到的基本命令：如 镜像查询、镜像拉取、镜像删除、创建容器、启动容器、停止容器、删除容器、动态查看日志、进入容器等。
<br>
<br>
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191110094604442.png)
<br>
这里需要说下项目结构。后端框架都是flask，但是分了两个后端。原因是在做动态日志的时候后端使用了flask-socketio这个库，而进入容器操作其实就是一个web terminal，这个功能参考网上使用了flask-sockets库,这两个库不兼容无法同时使用。

### 项目部署

<br>
通过项目根目录下的docker-compose.yaml启动服务，启动之前将后端项目中的config目录拷贝到根目录下用做配置文件挂载。
<br>
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191110103931968.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191110104000745.png)
<br>
在后端项目中，config目录下是所有的配置文件。其中hosts.yaml文件配置的是要管理的服务器。每个服务器有两个属性，host是访问域名或IP，certification是目标服务器是否会对docker api 进行鉴权（如何开启远程api访问和鉴权可去docker官网查询相关资料）。如果是需要鉴权的服务器，需要在certification目录下建一个以被鉴权服务器host为名称的文件夹，将cert.pem和key.pem文件放在下面即可。


### 工具介绍
#### 资源总览
实现对服务器基本信息的查看
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191110095528690.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70)
#### 镜像管理
当前所选服务器的 镜像列表查询、镜像删除、创建容器
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191110095811963.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70)
镜像查询、镜像拉取
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191110095914372.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70)
创建容器
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191110100021932.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70)
#### 容器管理
当前所选服务器的容器列表查询、容器启动、停止、删除
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191110100329916.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70)
查看实时日志
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191110100418759.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70)
web terminal（进入容器执行命令）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191110100627380.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70)

## 客户端

```docker-manager-client```是docker manager的客户端版本。
目前只是使用 electron 嵌入了web端的地址。

效果如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191118190856415.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NDUwNDg0,size_16,color_FFFFFF,t_70)






----------


[若图片无法查看请点击这里](https://blog.csdn.net/qq_36450484/article/details/102994570)









