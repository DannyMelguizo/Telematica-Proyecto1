import config_file, data_files
import grpc
import socket
import threading
from protobufs import services_pb2, services_pb2_grpc
from concurrent import futures

connections = []

def main():
    config_file.create_config_file()
    data_files.create_data_file()

    threading.Thread(target=server_grpc()).start()

    ip = config_file.get_ip()
    port = config_file.get_port()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen()

    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket,client_address)).start()


def server_grpc():
    port = config_file.get_port_grpc()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_ServicesServicer_to_server(Services(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()

def handle_client(client_socket, client_address):
    print(f"Connection from {client_address} has been established.")
    print(client_socket)



    

class Services(services_pb2_grpc.ServicesServicer):
    def SendNode(self, request, context):
        name = request.name

        nodes = ['szs', 'szs2', 'szs3']
        print(f"File {name} requested")

        return services_pb2.Nodes(nodes=nodes)

    def ManageFile(self, request, context):
        size = request.size
        name = request.name
        nodes = ['szs', 'szs2', 'szs3']
        block_size = 256*1024 # 256KB

        blocks = (size + block_size - 1) // block_size

        print(f"File {name} with size {size} bytes received")
        data_files.add_file(name, size, blocks)

        return services_pb2.NodesToSend(blocks=block_size, nodes=nodes)
    
    def GetFiles(self, request, context):
        files = data_files.get_files()
        return services_pb2.GetFilesResponse(files=files)



if __name__ == '__main__':
    main()