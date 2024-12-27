FROM apache/airflow:latest

USER root

RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

USER airflow
