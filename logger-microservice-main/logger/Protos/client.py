import grpc
from logger_pb2_grpc import LoggerServiceStub

channel = grpc.insecure_channel("localhost:50051")
client = LoggerServiceStub(channel)