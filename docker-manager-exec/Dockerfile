FROM python:3.6-slim

MAINTAINER guojiaxing<302802003@qq.com>

EXPOSE 5006

COPY . ./docker-manager-exec/

WORKDIR /docker-manager-exec/

RUN ["pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "-r", "requirements.txt"]

CMD ["python", "exec.py"]
