FROM python:3.6

MAINTAINER guojiaxing<302802003@qq.com>

EXPOSE 5005

COPY . ./docker-manager-flask/

WORKDIR /docker-manager-flask/

RUN ["pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "-r", "requirements.txt"]

CMD ["python", "app.py"]
