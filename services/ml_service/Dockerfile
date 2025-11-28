FROM python:3.11-slim

COPY . /ml_service
VOLUME /models
WORKDIR /ml_service

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]