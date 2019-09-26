FROM bde2020/spark-python-template:2.4.3-hadoop2.7

RUN pip3 install awscli boto3 pretty_midi config

COPY ./test_boto3.py /app

ENV SPARK_APPLICATION_PYTHON_LOCATION /app/test_boto3.py
ENV SPARK_APPLICATION_ARGS ""