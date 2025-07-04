FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install Flask mysql-connector-python

ENV MYSQL_HOST=database \
    MYSQL_USER=root \
    MYSQL_PASSWORD=kali \
    MYSQL_DB=reservation

EXPOSE 80

CMD ["python", "app.py"]

