import config_file
import re
import socket
import json
import threading

peers = []

def main():
    config_file.create_config_file()
    print("Welcome to the DataNode.")
    ip = input("Enter the IP of the Server:")

    while validate_ip(ip) == False:
        if ip == "localhost":
            break
        ip = input("Enter a valid IP: ")
    
    config_file.set_ip(ip)
    threading.Thread(target=server).start()

    connect_to_server()
    asign_node("file.txt", 1)




def connect_to_server(data = None):
    port = config_file.get_port()
    ip = config_file.get_ip()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))

    if data:
        server.send(data)
    else:
        while True:
            data = server.recv(1024).decode()
            print(data)
            if data == "first":
                break
            else:
                data = data.split(',')
                print(data)
                for ip in data:
                    connect_to_node(ip)
                break
    server.close()

def server():
    port = config_file.get_port()
    ip = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen()

    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=hanlded_client, args=(client_socket, client_address)).start()

def hanlded_client(client_socket, client_address):
    if len(peers) == 2:
        peers[1] = client_address[0]
    else:
        peers.append(client_address[0])
    print(peers)
    client_socket.close()

def asign_node(file_name, block):

    data = {
        "file_name": file_name,
        "block": block
    }

    data = json.dumps(data).encode()

    connect_to_server(data)

def connect_to_node(ip):
    port = config_file.get_port()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))
    server.close()
    peers.append(ip)
    
def validate_ip(ip):
    pattern = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

    if ip == "0.0.0.0":
        return False

    #Verify if the ip given is valid
    if re.match(pattern, ip):
        return True
    else:
        return False


if __name__ == '__main__':

    main()