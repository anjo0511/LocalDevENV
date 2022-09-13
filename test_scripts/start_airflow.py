
import psycopg2
from dotenv import dotenv_values
from python_on_whales import DockerClient
import logging
import os

base_path = '/Users/anjo/Arelion/LocalDevENV/docker_compose'

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s ---  %(message)s')

config = dotenv_values(os.path.join(base_path,"postgres/.env"))
airflow_config = dotenv_values(os.path.join(base_path,"airflow/.env"))

logging.info("Getting .env values from postgres and airflow dirs.")


conn = psycopg2.connect(host     = "localhost",
                        database = config.get('PG_DB'),
                        port     = config.get('PG_PORT'),
                        user     = config.get('PG_USR'),
                        password = config.get('PG_PW'))

cur = conn.cursor()

cur.execute('SELECT datname FROM pg_database;')
dbs_availible = [x[0] for x in cur.fetchall()]

if airflow_config.get('AIRFLOW_DB') not in dbs_availible:
    logging.info("Database: airflow not availible")
    cur.execute(f"CREATE DATABASE {airflow_config.get('AIRFLOW_DB')};")
else:
    logging.info("Database: airflow availible, nothing done")

cur.execute("SELECT usename FROM pg_catalog.pg_user;")
users_availible = [x[0] for x in cur.fetchall()]

if airflow_config.get('AIRFLOW_USR') not in users_availible:
    logging.info("User: airflow is not availible")
    cur.execute(f"CREATE USER {airflow_config.get('AIRFLOW_USR')} WITH PASSWORD {airflow_config.get('AIRFLOW_USR_PW')}")
    cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {airflow_config.get('AIRFLOW_DB')} TO {airflow_config.get('AIRFLOW_USR_PW')};")
else:
    logging.info("User: airflow availible, nothing done")

cur.close()


docker = DockerClient(compose_files=[os.path.join(base_path,"airflow/docker-compose.yml")], compose_profiles=["init", "flower"])
#docker.compose.up(detach=True)
docker.compose.down()
