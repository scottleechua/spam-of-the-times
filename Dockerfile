FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:server