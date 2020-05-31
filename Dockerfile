FROM python:3.7-alpine
MAINTAINER Anh 


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 0

# copy project
RUN mkdir /app
WORKDIR /app
ADD . /app/

# copy entrypoint.sh
COPY ./entrypoint.sh /app/

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
