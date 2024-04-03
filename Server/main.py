import config_file, data_files
import grpc
import socket
import threading
from protobufs import services_pb2, services_pb2_grpc
from concurrent import futures
import json
import random
import sys

connections = []

def main():

    config_file.create_config_file()
    data_files.create_data_file()

    ip = "0.0.0.0"
    port = config_file.get_port()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        grpc_server = threading.Thread(target=server_grpc)
        grpc_server.daemon = True
        grpc_server.start()

        server.bind((ip, port))
        server.listen()

        while True:
            client_socket, client_address = server.accept()
        
            thread = threading.Thread(target=handle_client, args=(client_socket,client_address))
            thread.daemon = True
            thread.start()

    except KeyboardInterrupt:
        print("Exiting server")
        server.close()
        sys.exit(0)


def server_grpc():
    port = config_file.get_port_grpc()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_ServicesServicer_to_server(Services(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()

def handle_client(client_socket, client_address):
    if client_address[0] not in connections:
        connections.append(client_address[0])
        print(f"New DataNode connected: {client_address[0]}")
    
    data = client_socket.recv(1024).decode()
    
    while data == '':
        data = client_socket.recv(1024).decode()

    print(f"Data received from {client_address[0]}: {data}")

    if data == "connect":
        if len(connections) == 1:
            client_socket.send(b"first")
        else:
            first_node = connections[0]
            penultimate = connections[-2]
            client_socket.send(f"{first_node},{penultimate}".encode())
        
    elif data == "save_data":
        client_socket.send(b'Ok')
        data = client_socket.recv(1024).decode()
        while data == '':
            data = client_socket.recv(1024).decode()

        try:
            data = json.loads(data)     
            file_name = data['file_name']
            block = data['block']

            print(f"Data received: {file_name}, {block}, {client_address[0]}")

            data_files.add_node(file_name, block, client_address[0])
        except:
            print("Invalid data received")


class Services(services_pb2_grpc.ServicesServicer):
    def SendNode(self, request, context):
        name = request.name

        nodes = data_files.get_nodes(name)

        print(f"File {name} requested")

        keys = json.dumps(list(nodes.keys()))
        values = json.dumps(list(nodes.values()))

        return services_pb2.Nodes(keys=bytes(keys, 'utf-8'), values=bytes(values, 'utf-8'))

    def ManageFile(self, request, context):
        size = request.size
        name = request.name
        block_size = 256*1024 # 256KB

        blocks = (size + block_size - 1) // block_size 

        nodes = []
        nodes_available = connections.copy()
        
        for i in range(blocks):
            if len(nodes_available) == 0:
                nodes_available = connections.copy()
            node = random.choice(nodes_available)
            nodes.append(node)
            nodes_available.remove(node)

        print(f"File {name} with size {size} bytes received")
        data_files.add_file(name, size, blocks)

        return services_pb2.NodesToSend(blocks=block_size, nodes=nodes)
    
    def GetFiles(self, request, context):
        files = data_files.get_files()
        return services_pb2.GetFilesResponse(files=files)



if __name__ == '__main__':
    main()