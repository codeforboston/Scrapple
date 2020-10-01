FROM python:3-onbuild

RUN apt-get update && install -y postgresql && clean

CMD sh /app/docker_start.sh
