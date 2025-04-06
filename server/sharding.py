class ShardedKVStore:
    def __init__(self, nodes):
        self.nodes = nodes  # List of ("host", port) tuples
        self.num_nodes = len(nodes)

    def _get_node(self, key):
        """Simple hash-based sharding."""
        return hash(key) % self.num_nodes

    def get(self, key):
        node_idx = self._get_node(key)
        host, port = self.nodes[node_idx]
        client = KVStoreClient(host, port)
        return client.get(key)

    def put(self, key, value):
        node_idx = self._get_node(key)
        host, port = self.nodes[node_idx]
        client = KVStoreClient(host, port)
        return client.put(key, value)

    def delete(self, key):
        node_idx = self._get_node(key)
        host, port = self.nodes[node_idx]
        client = KVStoreClient(host, port)
        return client.delete(key)