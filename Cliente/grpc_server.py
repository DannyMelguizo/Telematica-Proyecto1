import os
import grpc
import config_file, mom_server
import json

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
    current = 1
    for node in nodes:
        current_block = f"{name_file}.{current}"
        
        with open(current_block, 'rb') as file:
            mom_server.send_block(node, file.read())

        os.remove(current_block)
        current += 1

def get_file(name_file, ip):
    global port

    nodes = {}

    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = services_pb2_grpc.ServicesStub(channel)
        response = stub.SendNode(services_pb2.NameFile(name=name_file))
        decode_keys = response.keys.decode('utf-8')
        decode_values = response.values.decode('utf-8')

        keys = json.loads(decode_keys)
        values = json.loads(decode_values)

        nodes = dict(zip(keys, values))

    # Get the blocks
    for block in nodes:

        for node in nodes[block]:
            # try:
            with grpc.insecure_channel(f'{node}:{port}') as channel:
                stub = services_pb2_grpc.ServicesStub(channel)

                stub.SendBlock(services_pb2.GetBlock(ip=config_file.get_ip(), file=name_file,  block=int(block)))

            #         break
            # except:
            #     print(f"Node {node} is not available")

    # Rebuild the file
    # rebuild_file(name_file)
                
def save_block(body):
    data = body.split(b'\n')
    name_file = data[0]
    blocks = data[2]
    block = blocks.split(b'/')[0]

    block_name = f"{name_file.decode('utf-8')}.{block.decode('utf-8')}"

    with open(block_name, 'wb') as file:
        file.write(body)


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