import config_file, mom_server, grpc_server
import re
import socket
import json
import threading


def main():
    config_file.create_config_file()
    print("Welcome to the DataNode.")
    ip = input("Enter the IP of the Server:")

    while validate_ip(ip) == False:
        if ip == "localhost":
            break
        ip = input("Enter a valid IP: ")
    
    config_file.set_ip_server(ip)
    threading.Thread(target=server).start()
    connect_to_server("connect")
    
    threading.Thread(target=mom_server.get_blocks).start()
    threading.Thread(target=grpc_server.server_grpc).start()

def connect_to_server(option, data = None):
    port = config_file.get_port()
    ip = config_file.get_ip_server()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))

    if option == "save_data":
        server.send(option.encode())
        data_confirm = server.recv(1024).decode()
        while data_confirm != 'Ok':
            data_confirm = server.recv(1024).decode()
        server.send(data)


    elif option == "connect":
        
        server.send(option.encode())

        data = server.recv(1024).decode()
        while data == '':
            data = server.recv(1024).decode()

        if data != "first":
            data = data.split(',')
            for ip in data:
                connect_to_node(ip)
            
    server.close()

def server():
    port = config_file.get_port()
    ip = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen()
    print(f"Server running on {ip}:{port}")

    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

def handle_client(client_socket, client_address):
    config_file.add_peer(client_address[0])

    client_socket.close()

def asign_node(file_name, block):

    data = {
        "file_name": file_name,
        "block": block
    }

    data = json.dumps(data).encode()

    connect_to_server("save_data", data)

def connect_to_node(ip):
    port = config_file.get_port()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))
    server.close()
    config_file.add_peer(ip)
    
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