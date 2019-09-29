FROM python:3-alpine

WORKDIR /app

COPY . /app/

# Proxy configurations
# ENV http_proxy 8080:8080
# ENV https_proxy 8080:8080

ENV NAME Amazing World!

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]
