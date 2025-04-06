import grpc
from kv_store_pb2 import GetRequest, PutRequest, DeleteRequest
from kv_store_pb2_grpc import KeyValueStoreStub

class KVStoreClient:
    def __init__(self, host="localhost", port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = KeyValueStoreStub(self.channel)

    def get(self, key):
        response = self.stub.Get(GetRequest(key=key))
        return response.value if response.success else None

    def put(self, key, value):
        response = self.stub.Put(PutRequest(key=key, value=value))
        return response.success

    def delete(self, key):
        response = self.stub.Delete(DeleteRequest(key=key))
        return response.success

if __name__ == "__main__":
    client = KVStoreClient()
    print(client.put("name", "Alice"))  # True
    print(client.get("name"))           # "Alice"
    print(client.delete("name"))        # True