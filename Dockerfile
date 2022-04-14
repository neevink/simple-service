FROM python:3

WORKDIR /usr/src/simple-service

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3.8", "./app/app.py" ]