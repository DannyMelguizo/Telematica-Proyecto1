import pika
import config_file

port = config_file.get_port_mom()

def get_blocks():
    global port

    ip = config_file.get_ip()
    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port))
    channel = connection.channel()

    channel.queue_declare(queue=ip)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
    
    channel.basic_consume(queue=ip, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def send_block(ip, block):
    global port

    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, port))
    channel = connection.channel()

    channel.queue_declare(queue=ip)

    channel.basic_publish(exchange='', routing_key=ip, body=block)
    print(f" [x] Sent block'")

    connection.close()