import configparser
import requests

config = configparser.ConfigParser()

def create_config_file():
    ip = public_ip()
    proto_path = 'protobufs/service.proto'

    config['config'] = {
        'ip': ip,
        'ip_server': '',
        'port': '8000',
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

def set_ip_server(ip):
    config['config']['ip_server'] = ip

    with open('config.conf', 'w') as archivo:
        config.write(archivo)

def get_config():
    config.read('config.conf')

    return config

def get_ip():
    return get_config()['config']['ip']

def get_ip_server():
    return get_config()['config']['ip_server']

def get_port_grpc():
    return int(get_config()['config']['port_grpc'])

def get_port_mom():
    return int(get_config()['config']['port_mom'])

def get_port():
    return int(get_config()['config']['port'])

def add_peer(ip):

    config = get_config()

    if config.has_section('peers') == False:
        config.add_section('peers')
        config['peers']['peer1'] = ip
    else:
        config['peers']['peer2'] = ip
    
    with open('config.conf', 'w') as archivo:
        config.write(archivo)

def get_peers():
    return get_config()['peers'].values()