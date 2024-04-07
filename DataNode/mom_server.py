import pika
import config_file, main
import shutil
import os
import random

port = config_file.get_port_mom()

def get_blocks():
    global port

    ip = config_file.get_ip()
    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port))
    channel = connection.channel()

    channel.queue_declare(queue='blocks')

    def callback(ch, method, properties, body):
        print(f" [x] Received")

        if not os.path.exists('blocks'):
            os.makedirs('blocks')
        
        data = body.split(b'\n')

        name_file = data[0]
        blocks = data[2]
        block = blocks.split(b'/')[0]
        replica = data[3]

                
        if replica == b'0':
            connections = []
            peers = config_file.get_peers()
            for peer in peers:
                connections.append(peer)
            
            random_peer = random.choice(connections)
            data[3] = b'1'
            
            data_reconstructed = b''
            for d in data:
                data_reconstructed += d + b'\n'
            
            replicate_block(random_peer, data_reconstructed)

        block_name = f"{name_file.decode('utf-8')}.{block.decode('utf-8')}"

        if not os.path.exists(f'blocks/{block_name}'):

            with open(block_name, 'wb') as file:
                file.write(body)
            
            shutil.move(block_name, 'blocks')

            main.asign_node(name_file.decode('utf-8'), block.decode('utf-8'))

    channel.basic_consume(queue='blocks', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def send_block(ip, block, file):
    global port

    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port))
    channel = connection.channel()

    channel.queue_declare(queue='sent_blocks')

    block_name = f"{file}.{block}"

    file_path = f'blocks/{block_name}'

    with open(file_path, 'rb') as file:

        channel.basic_publish(exchange='', routing_key='sent_blocks', body=file.read())
        print(f" [x] Sent")

        connection.close()

def replicate_block(ip, file):
    global port

    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port))
    channel = connection.channel()

    channel.queue_declare(queue='blocks')

    channel.basic_publish(exchange='', routing_key='blocks', body=file)
    print(f" [x] Replicated")

    connection.close()