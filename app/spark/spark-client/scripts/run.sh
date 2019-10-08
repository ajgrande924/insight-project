#!/bin/bash

# bail out if anything fails
set -e

run_spark_submit () {
  /spark/bin/spark-submit \
  --driver-class-path /jars/org.postgresql_postgresql-42.1.1.jar \
  --conf spark.executor.extraClassPath=/jars/org.postgresql_postgresql-42.1.1.jar \
  --jars /jars/org.postgresql_postgresql-42.1.1.jar \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --conf spark.driver.host=spark-client /examples/python/$1
}

run_spark_full () {
  run_spark_submit main.py
}

run_spark_subset () {
  run_spark_submit main_subset.py
}

"$@"
