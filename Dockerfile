ARG image_name=ubuntu:16.04
ARG username=root
FROM $image_name

USER root

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential curl sudo
RUN curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
RUN apt-get install -y nodejs

EXPOSE 8082

RUN mkdir -p /home/project_files
COPY . /app
WORKDIR /app
RUN cd static
RUN npm install
RUN cd ..
RUN pip install -r requirements.txt --no-cache-dir
CMD python -u terminal_provider.py

USER $username
