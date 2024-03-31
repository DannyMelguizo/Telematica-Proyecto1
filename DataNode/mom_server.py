import pika
import config_file, main
import os

port = config_file.get_port_mom()

def get_blocks():
    global port

    ip = config_file.get_ip()
    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port))
    channel = connection.channel()

    channel.queue_declare(queue='blocks')

    def callback(ch, method, properties, body):
        print(f" [x] Received")
        
        body = body.split(b'\n')

        name_file = body[0]
        blocks = body[2]

        block = blocks.split('/')[0]

        with open(f"files/{name_file}.{block}", 'wb') as file:
            file.write(body)

        main.asign_node(name_file, block)

    
    channel.basic_consume(queue=ip, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()