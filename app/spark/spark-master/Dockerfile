FROM ajgrande924/spark-base:latest

MAINTAINER AJ Grande <ajgrande924@gmail.com>

COPY spark-master.sh /

ENV SPARK_MASTER_PORT 7077
ENV SPARK_MASTER_WEBUI_PORT 8080
ENV SPARK_MASTER_LOG /spark/logs

EXPOSE 8080 7077 6066

CMD ["/bin/bash", "/spark-master.sh"]