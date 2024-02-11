FROM python:3.11-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
ADD https://github.com/scottleechua/data/blob/main/spam-and-other-messages/text-messages.csv?raw=true ./
EXPOSE 8080
CMD exec gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 8 --timeout 0 app:server