import os
import grpc
import config_file, mom_server

from protobufs import services_pb2, services_pb2_grpc

port = config_file.get_port_grpc()

def send_file(name_file, ip):
    global port
    file_path = f'files/{name_file}'
    size_file = os.path.getsize(file_path)
    block_size = 0
    nodes = []

    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = services_pb2_grpc.ServicesStub(channel)

        response = stub.ManageFile(services_pb2.UploadFile(name=name_file, size=size_file))
        block_size = response.blocks
        nodes = response.nodes
    
    total_blocks = (size_file + block_size - 1) // block_size

    with open(file_path, 'rb') as file:

        for i in range(total_blocks):
            data = file.read(block_size)
            block_name = f"{name_file}.{i+1}"

            with open(block_name, 'wb') as block:
                block.write(f"{name_file}\n".encode())
                block.write(f"{size_file}\n".encode())
                block.write(f"{i+1}/{total_blocks}\n".encode())
                block.write(data)
                print(f"Block {i+1} of {total_blocks} created")

    # Send File to the given nodes
    print(f"Sending file {name_file} to nodes {nodes}")
    current = 1
    for node in nodes:
        current_block = f"{name_file}.{current}"
        
        with open(current_block, 'rb') as file:
            mom_server.send_block(node, file.read())

        os.remove(current_block)
        current += 1

def get_file(name_file, ip):
    global port
    nodes = []
    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = services_pb2_grpc.ServicesStub(channel)
        response = stub.SendNode(services_pb2.NameFile(name=name_file))

        nodes = response.nodes

    print(f"The nodes: {nodes} have blocks of the file {name_file}")

    # Get the blocks
    for block in nodes:
        print(f"Getting block {block} from nodes {nodes[block]}")

    # Rebuild the file
    rebuild_file(name_file)

def rebuild_file(name_file):
    blocks = []
    file_path = f'files/{name_file}'

    for filename in os.listdir('.'):

        if filename.startswith(name_file):
            blocks.append(filename)

    # Sort blocks by its number
    blocks.sort(key=lambda x: int(x.rsplit('.', 1)[1]))

    data_reconstructed = b""
    for block in blocks:
        with open(block, 'rb') as f:
            name_file, size_file, position = f.readline().decode().strip(), int(f.readline().decode().strip()), f.readline().decode().strip()
            data_reconstructed += f.read()
        
    with open(file_path, 'wb') as f:
        f.write(data_reconstructed)

def list_files(ip):
    global port
    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = services_pb2_grpc.ServicesStub(channel)

        response = stub.GetFiles(services_pb2.GetFilesRequest())

        return response.files