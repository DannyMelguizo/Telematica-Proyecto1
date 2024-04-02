import pika
import config_file, main
import shutil
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

        if not os.path.exists('blocks'):
            os.makedirs('blocks')
        
        data = body.split(b'\n')

        name_file = data[0]
        blocks = data[2]
        block = blocks.split(b'/')[0]

        block_name = f"{name_file.decode('utf-8')}.{block.decode('utf-8')}"

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

    channel.queue_declare(queue='sent_block')

    block_name = f"{file}.{block}"

    data = b''

    with open(f'\\blocks\\{block_name}', 'rb') as file:
        data = file.read()

    channel.basic_publish(exchange='', routing_key=ip, body=data)
    print(f" [x] Sent block to {ip}")

    connection.close()