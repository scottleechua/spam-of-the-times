FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY pyproject.toml uv.lock ./
RUN pip install uv
# Remove legacy Dash packages before install
RUN uv pip uninstall -y \
    dash-table \
    dash-renderer \
    dash-core-components \
    dash-html-components || true
RUN uv sync --no-cache
COPY . ./
ADD https://raw.githubusercontent.com/scottleechua/data/main/spam-and-marketing-sms/text-messages.csv ./
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "0", "app:server"]