FROM apache/airflow:2.3.3-python3.10

WORKDIR /opt/airflow
USER root

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libpq-dev build-essential iputils-ping libffi-dev python-dev git cifs-utils

USER airflow

RUN pip install --upgrade wheel setuptools psycopg2 cryptography

COPY requirements.txt /opt/airflow/requirements.txt
RUN pip install -r /opt/airflow/requirements.txt