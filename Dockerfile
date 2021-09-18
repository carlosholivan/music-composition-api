FROM matthewfeickert/docker-python3-ubuntu:3.8.7

USER root

RUN sudo apt-get update
RUN sudo apt-get install -y libsndfile-dev ffmpeg

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --src /usr/local/src

COPY . .

CMD FLASK_APP=webserver FLASK_ENV=production FLASK_RUN_PORT=8080 flask run --host=0.0.0.0
