#!/bin/bash

# bail out if anything fails
set -e

docker login -u ${USER}

set -e

SPARK_VERSION=2.4.4
HADOOP_PROFILE=2.7
HADOOP_VERSION=2.7.3
KUBERNETES_VERSION=4.4.2
SCALA_VERSION=2.11
DOCKER_REPOSITORY=${USER}
TAG=spark-${SPARK_VERSION}

echo "Install requirement packages"
apk add --virtual --update --no-cache curl jq python py-pip bash dpkg openjdk8
update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/java-1.8-openjdk/bin/javac 1
update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-1.8-openjdk/bin/java 1

echo "Downloading Spark source code"
mkdir -p /opt/spark/ && cd $_
wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}.tgz -O - | tar -xz

echo "Switching dir"
cd spark-${SPARK_VERSION}/

echo "Changing Kubernetes client version"
echo $KUBERNETES_VERSION | xargs -i{} sed -i -r 's/(<kubernetes.client.version>)(.*)(<\/kubernetes.client.version>)/\1{}\3/' resource-managers/kubernetes/core/pom.xml

echo "Building Spark"
./build/mvn -Phadoop-${HADOOP_PROFILE} -Dhadoop.version=${HADOOP_VERSION} -Pkubernetes -Pscala-${SCALA_VERSION} -DskipTests clean package

echo "Building Spark Docker image"
./bin/docker-image-tool.sh -r ${DOCKER_REPOSITORY} -t ${TAG} build

echo "Pushing Spark Docker image"
./bin/docker-image-tool.sh -r ${DOCKER_REPOSITORY} -t ${TAG} push

echo "Pushed Spark Docker image! Terminating container..."