FROM python:alpine

EXPOSE 80
# set proper ENV to run app on docker
ENV FLASK_RUN_HOST="0.0.0.0"
ENV PIP_NO_CACHE_DIR="true"

ENV LAGUINHO_MONGO_HOST="localhost"
ENV LAGUINHO_MONGO_PORT="27017"
ENV LAGUINHO_DB_NAME="laguinho"
ENV LAGUINHO_MONGO_USERNAME="opendevufcg"
ENV LAGUINHO_MONGO_PASSWORD="laguinhoapi"
ENV LAGUINHO_MONGO_AUTH_SOURCE="admin"

WORKDIR /opt

# copy project files to /opt
COPY . /opt/

# installs pipenv, and gcc to compile required cython and then purge it to save space.
# this is needed to run on a single RUN to create only one container layer.
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
 && pip install pipenv \
 && pipenv install waitress \
 && pipenv install --deploy --system \
 && apk del .build-deps

ENTRYPOINT ["pipenv", "run", "waitress-serve", "--port=80", "--call", "laguinho:create_app"]
