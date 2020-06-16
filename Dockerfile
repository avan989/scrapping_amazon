FROM python:3.7.6-buster
MAINTAINER Anh 

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 0

RUN pip install --upgrade pip
RUN pip install requests bs4 lxml
RUN pip install pandas nltk
 
# copy project
RUN mkdir /app
WORKDIR /app
ADD . /app/

# copy entrypoint.sh
COPY ./entrypoint.sh /app/

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
