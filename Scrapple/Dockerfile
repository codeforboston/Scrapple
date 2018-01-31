FROM python:3-onbuild

RUN apt-get update && \
    apt-get install -y postgresql && \
    apt-get clean

CMD sh /app/docker_start.sh
