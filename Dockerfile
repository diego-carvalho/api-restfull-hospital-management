FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN pip install flask
RUN pip install flask-mysql

COPY ./app /app
