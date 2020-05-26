FROM python:3.6.8-slim
RUN useradd --create-home --no-log-init --shell /bin/bash fusiontree
RUN adduser fusiontree sudo

RUN sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list \
    && rm -Rf /var/lib/apt/lists/* && apt-get update && apt-get install vim -y \
    && apt-get install -y libc6-dev gcc mime-support


WORKDIR /app
RUN chown fusiontree:fusiontree /app
USER fusiontree
ENV PYTHONUNBUFFERED 1
ENV PATH $PATH:/home/fusiontree/.local/bin

COPY . /app/
RUN pip install --user  -i "https://pypi.tuna.tsinghua.edu.cn/simple" pipenv && pipenv install

CMD ["pipenv","run","python","-m","utils"]
