FROM python:3.9-slim

ENV TZ Asia/Tehran
EXPOSE 8000

RUN apt update && apt install -y make

ENV PYTHONUNBUFFERED=miomio

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN echo yes | dangidongi/manage.py collectstatic


ENTRYPOINT [ "sh", "-c", "export DJANGO_SETTINGS_MODULE=dangidongi.settings && gunicorn --bind :8000 --workers 2 dangidongi.wsgi:application" ]
