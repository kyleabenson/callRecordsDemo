

from concurrent import futures
import logging
import os
import grpc
import calls_pb2
import calls_pb2_grpc

from opentelemetry import trace
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(CloudTraceSpanExporter(os.environ['GCP_PROJECT']))
)

grpc_server_instrumentor = GrpcInstrumentorServer()
grpc_server_instrumentor.instrument()



class recorder(calls_pb2_grpc.recorderServicer):

    def ingestRecord(self, request, context):
        return calls_pb2.ackRecord(message=f"{request.FullName , request.PhoneNumber}")        

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calls_pb2_grpc.add_recorderServicer_to_server(recorder(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
    