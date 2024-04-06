import pika
import config_file, grpc_server

port = config_file.get_port_mom()

def get_blocks():
    global port

    ip = config_file.get_ip()

    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port))
    channel = connection.channel()

    channel.queue_declare(queue='sent_blocks')

    def callback(ch, method, properties, body):
        grpc_server.save_block(body)

    channel.basic_consume(queue='sent_blocks', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def send_block(ip, block):
    global port

    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port))
    channel = connection.channel()

    channel.queue_declare(queue='blocks')

    channel.basic_publish(exchange='', routing_key='blocks', body=block)

    connection.close()