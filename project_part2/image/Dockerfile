FROM python:3-alpine

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

ENV FLASK_APP=server.py
ENV FLASK_RUN_PORT=1080

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 1080

CMD ["python", "app.py"]
