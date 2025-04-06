import threading
from concurrent import futures
import grpc
from kv_store_pb2 import GetResponse, PutResponse, DeleteResponse
from kv_store_pb2_grpc import KeyValueStoreServicer, add_KeyValueStoreServicer_to_server

class KVStoreServicer(KeyValueStoreServicer):
    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()

    def Get(self, request, context):
        key = request.key
        with self.lock:
            value = self.store.get(key, "")
            success = key in self.store
        return GetResponse(value=value, success=success)

    def Put(self, request, context):
        key, value = request.key, request.value
        with self.lock:
            self.store[key] = value
        return PutResponse(success=True)

    def Delete(self, request, context):
        key = request.key
        with self.lock:
            success = key in self.store
            if success:
                del self.store[key]
        return DeleteResponse(success=success)

def serve(port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_KeyValueStoreServicer_to_server(KVStoreServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server running on port {port}")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()