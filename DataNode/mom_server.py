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
        block = blocks.split(b'/')[0]

        block_name = f"{name_file.decode('utf-8')}.{block.decode('utf-8')}"

        print(f"Block name: {block_name}")

        with open(f"blocks/{block_name}", 'wb') as file:
            file.write(body)

        main.asign_node(name_file, block)

    
    channel.basic_consume(queue=ip, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()