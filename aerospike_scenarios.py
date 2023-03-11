from typing import Dict, Any

import aerospike

from scenarios import ProductStoreScenario

LOCALHOST = {
    'hosts': [('127.0.0.1', 3000)],
    "policies": {
        "login_timeout_ms": 10000
    },
    "connect_timeout": 10000,
}


def new_aerospike_client(config: Dict[str, Any]) -> aerospike.Client:
    return aerospike.client(config).connect()


class AerospikeProductStoreScenario:
    NS = 'test'
    SET = 'products'

    def __init__(self, config, num_products, num_queries):
        self.client: aerospike.Client = new_aerospike_client(config)
        self.scenario = ProductStoreScenario(num_products, num_queries)

    def execute(self):
        self._clean()
        self.scenario.execute(self)

    def _clean(self):
        # Setting nanos=0 will delete all entries in the set
        self.client.truncate(self.NS, self.SET, nanos=0)

    def load_products(self, products):
        for product in products:
            key = (self.NS, self.SET, product['product_id'])
            self.client.put(key, product)

    def get_product_title(self, product_id):
        key = (self.NS, self.SET, product_id)
        key2, meta, bins = self.client.get(key)
        return bins['title']

    def get_product_desc(self, product_id):
        key = (self.NS, self.SET, product_id)
        key2, meta, bins = self.client.get(key)
        return bins['description']
