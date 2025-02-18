FROM python:3.12-alpine

WORKDIR /app
COPY ./app .
RUN apk upgrade --no-cache  \
 && pip install --upgrade pip \
 && pip install -r requirements.txt

CMD ["python3", "main.py"]
