FROM python:3.10.5-alpine3.15

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

CMD python main.py
