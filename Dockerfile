FROM python:3.11-alpine
WORKDIR /app
COPY . /app
RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip3 install -r requirements.txt

ENV PYTHONPATH=/app
CMD ["sh", "-c", "python3 bot_runner.py & python3 web/app.py"]