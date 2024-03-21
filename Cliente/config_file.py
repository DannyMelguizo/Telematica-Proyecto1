import configparser
import requests

config = configparser.ConfigParser()

def create_config_file():
    ip = public_ip()
    proto_path = 'protobufs/service.proto'

    config['config'] = {
        'ip_public': f'{ip}',
        'port_grpc': '8001',
        'port_mom': '5672',
        'proto_path': f'{proto_path}'
    }

    #Create the file config.conf
    with open('config.conf', 'w') as archivo:
        config.write(archivo)

def public_ip():
    ip = requests.get("https://api.ipify.org").text
    return ip

def get_config():
    config.read('config.conf')

    return config

def get_ip():
    return get_config()['config']['ip_public']

def get_port_grpc():
    return int(get_config()['config']['port_grpc'])

def get_port_mom():
    return int(get_config()['config']['port_mom'])

