FROM tiangolo/uwsgi-nginx-flask:python3.10

COPY . /app

RUN pip3 install -r requirements.txt

WORKDIR /app

CMD ["python3", "app.py"]