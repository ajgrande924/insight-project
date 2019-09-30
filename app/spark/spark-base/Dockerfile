FROM bde2020/spark-base:2.4.3-hadoop2.7

MAINTAINER AJ Grande <ajgrande924@gmail.com>

RUN apk add --update python3 python3-dev gfortran py-pip build-base
RUN pip3 install --no-cache --upgrade pip && pip3 install awscli boto3 pretty_midi config
