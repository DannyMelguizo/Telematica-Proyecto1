import os
import grpc
import config_file, mom_server
import threading

from protobufs import services_pb2, services_pb2_grpc
from concurrent import futures

def server_grpc():
    port = config_file.get_port_grpc()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_ServicesServicer_to_server(Services(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()


class Services(services_pb2_grpc.ServicesServicer):
    def SendBlock(self, request, context):
        ip = request.ip
        block = request.block
        file = request.file
        
        threading.Thread(target=mom_server.send_block, args=(ip, block, file)).start()

        return services_pb2.GetBlockResponse()