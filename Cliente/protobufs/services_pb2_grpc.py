# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import services_pb2 as services__pb2


class ServicesStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendNode = channel.unary_unary(
                '/services.Services/SendNode',
                request_serializer=services__pb2.NameFile.SerializeToString,
                response_deserializer=services__pb2.Nodes.FromString,
                )
        self.ManageFile = channel.unary_unary(
                '/services.Services/ManageFile',
                request_serializer=services__pb2.UploadFile.SerializeToString,
                response_deserializer=services__pb2.NodesToSend.FromString,
                )
        self.GetFiles = channel.unary_unary(
                '/services.Services/GetFiles',
                request_serializer=services__pb2.GetFilesRequest.SerializeToString,
                response_deserializer=services__pb2.GetFilesResponse.FromString,
                )
        self.SendBlock = channel.unary_unary(
                '/services.Services/SendBlock',
                request_serializer=services__pb2.GetBlock.SerializeToString,
                response_deserializer=services__pb2.GetBlockResponse.FromString,
                )


class ServicesServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendNode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ManageFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFiles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendBlock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServicesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendNode': grpc.unary_unary_rpc_method_handler(
                    servicer.SendNode,
                    request_deserializer=services__pb2.NameFile.FromString,
                    response_serializer=services__pb2.Nodes.SerializeToString,
            ),
            'ManageFile': grpc.unary_unary_rpc_method_handler(
                    servicer.ManageFile,
                    request_deserializer=services__pb2.UploadFile.FromString,
                    response_serializer=services__pb2.NodesToSend.SerializeToString,
            ),
            'GetFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFiles,
                    request_deserializer=services__pb2.GetFilesRequest.FromString,
                    response_serializer=services__pb2.GetFilesResponse.SerializeToString,
            ),
            'SendBlock': grpc.unary_unary_rpc_method_handler(
                    servicer.SendBlock,
                    request_deserializer=services__pb2.GetBlock.FromString,
                    response_serializer=services__pb2.GetBlockResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'services.Services', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Services(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendNode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/services.Services/SendNode',
            services__pb2.NameFile.SerializeToString,
            services__pb2.Nodes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ManageFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/services.Services/ManageFile',
            services__pb2.UploadFile.SerializeToString,
            services__pb2.NodesToSend.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/services.Services/GetFiles',
            services__pb2.GetFilesRequest.SerializeToString,
            services__pb2.GetFilesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendBlock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/services.Services/SendBlock',
            services__pb2.GetBlock.SerializeToString,
            services__pb2.GetBlockResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
