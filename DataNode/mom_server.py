import pika
import config_file
import os

port = config_file.get_port_mom()

def get_blocks():
    global port

    ip = config_file.get_ip()
    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port))
    channel = connection.channel()

    channel.queue_declare(queue=ip)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

        body = body.decode()
        body = body.split('\n')
        file_name = body[0]
        size = body[1]
        block = body[2]
        data = body[3]

        print(f"Data received: {file_name}, {size}, {block}")

    
    channel.basic_consume(queue=ip, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()