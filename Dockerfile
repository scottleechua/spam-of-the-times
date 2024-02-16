FROM python:3.11-alpine
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/usr/local
ADD --chmod=655 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN /root/.cargo/bin/uv pip install --no-cache -r requirements.txt
COPY . ./
ADD https://raw.githubusercontent.com/scottleechua/data/main/spam-and-marketing-sms/text-messages.csv ./
EXPOSE 8080
CMD exec gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 8 --timeout 0 app:server