import Services.app as app

import grpc

import logger_pb2
import logger_pb2_grpc

import concurrent.futures as futures

from signal import signal, SIGTERM

class LoggerService(logger_pb2_grpc.LoggerService):
    def CreateLog(self, request, context):
        app.create_log(request)
    def ReadLog(self, request, context):
        app.read_logs()
    def ReadLogById(self, request, context):
        app.read_logs(request.user_id)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    logger_pb2_grpc.add_LoggerServiceServicer_to_server(
        LoggerService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    def handle_sigterm(*_):
        print("Received shutdown signal")
        all_rpcs_done_event = server.stop(30)
        all_rpcs_done_event.wait(30)
        print("Shut down gracefully")

    signal(SIGTERM, handle_sigterm)
    server.wait_for_termination()


if __name__ == "__main__":
    serve(threaded=True)