FROM python:3.9

WORKDIR /app

COPY requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt --no-cache-dir

COPY foodgram/ .

CMD ["gunicorn", "--bind", "0.0.0.0:9090", "foodgram.wsgi:application"]