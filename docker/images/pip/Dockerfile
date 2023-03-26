ARG DOCKER_REPOSITORY_ID
ARG BRANCH

FROM protyom/copart-bot:os

LABEL maintainer="protyom"

WORKDIR /app/
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt
