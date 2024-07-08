FROM python:latest

WORKDIR /app

COPY src /app/src

ENV PYTHONPATH=/app

RUN pip install -r src/requirements.txt

CMD ["python3", "src/app.py"]
