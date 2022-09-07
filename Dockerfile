FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y python3-opengl \
    python-tk \
    python3-tk \
    tk-dev
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]