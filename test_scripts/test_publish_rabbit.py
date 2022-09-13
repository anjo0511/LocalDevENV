import pika
import pika.exceptions
import ssl
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path('../rabbitmq/.env'))


credentials = pika.PlainCredentials(os.getenv('BROKER_USR'), os.getenv('BROKER_PW'))

#ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
#ssl_context.verify_mode = ssl.CERT_REQUIRED
#ssl_context.check_hostname = True
#ssl_context.load_default_certs()
#, ssl_options=pika.SSLOptions(ssl_context))

parameters = pika.ConnectionParameters(host='localhost', port='5672', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()  


channel.confirm_delivery() # optional

#channel.queue_declare(queue='aliveness-test')

for i in range(500):
    try:
        channel.basic_publish(exchange='',
                              routing_key='airflow_celery',
                              body=f'Hello World! {i}',
                              properties=pika.BasicProperties(content_type='text/plain',
                                                              delivery_mode=pika.DeliveryMode.Transient),
                                                              mandatory=True)
        print(f" [x][{i}] Sent 'Hello World!'")
        print('Message was published')
    except pika.exceptions.UnroutableError:
        print('Message was returned')

connection.close()