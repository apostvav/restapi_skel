FROM python:3.6-alpine

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
RUN mkdir -p /app
COPY restapi_skel /app/restapi_skel
COPY migrations /app/migrations
COPY app.py /app/app.py

WORKDIR /app

ENV FLASK_APP app.py
EXPOSE 5000

CMD ["gunicorn", "-b", ":5000", "app:app"]
