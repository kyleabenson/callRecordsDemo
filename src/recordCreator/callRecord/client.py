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
        stub = calls_pb2_grpc.RecordCallStub(channel)
        # response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
        response = stub.RecordIngest(calls_pb2.CallRecord(timestamp="today", FullName="Kyle Benson", PhoneNumber="1-888-555-555", CallType="inbound"))
    print("Greeter client received: " + response.AckRecord)


if __name__ == '__main__':
    logging.basicConfig()
    run()