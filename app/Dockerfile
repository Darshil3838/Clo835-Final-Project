FROM ubuntu:20.04
RUN apt-get update -y
WORKDIR /app
COPY . /app
RUN set -xe \
    && apt-get update -y \
    && apt-get install -y python3-pip \
    && apt-get install -y mysql-client 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install boto3
EXPOSE 81
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]