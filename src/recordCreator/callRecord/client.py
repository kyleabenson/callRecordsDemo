import logging

import grpc
import calls_pb2
import calls_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Make a simple request")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calls_pb2_grpc.recorderStub(channel)
        # response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
        response = stub.ingestRecord(calls_pb2.callerRecord(FullName="Kyle Benson"))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()