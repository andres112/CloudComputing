FROM python:3-alpine

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

ENV FLASK_APP = server.py
ENV FLASK_RUN_PORT = 1080
ENV DB_HOST = localhost
ENV DB_PORT = 3306
ENV DB_DBNAME = watches
ENV DB_USER = watches
ENV DB_PASS = watches
ENV HTTP_USER = cloud
ENV HTTP_PASS = computing

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 1080

CMD ["python", "server.py"]
