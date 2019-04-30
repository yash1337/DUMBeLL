FROM jfloff/alpine-python:latest
LABEL maintainer="developeraccys@gmail.com"

RUN mkdir /DUMBeLL
WORKDIR /DUMBeLL

COPY MutualExclusion /DUMBeLL
COPY ApplicationProcess /DUMBeLL
COPY requirements.txt /DUMBeLL







EXPOSE 80/tcp