FROM python:3.9

WORKDIR /app

COPY requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt --no-cache-dir

COPY Foodgram/ .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Foodgram.wsgi:application"]