FROM apache/airflow:2.3.3-python3.10

USER root

RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN apt-get install -y libffi-dev python-dev

USER airflow

RUN pip install --upgrade wheel setuptools psycopg2 cryptography
