FROM python:alpine

WORKDIR /app

COPY . .

RUN python -m pip install -r requirements.txt

CMD flask --app app run --host=0.0.0.0
