from typing import Dict, Any, Sequence

import aerospike
from dataclasses import asdict
from scenarios import ProductStoreScenarioImpl, Product

_DEFAULT_CONF = {
    "policies": {
        "login_timeout_ms": 10000
    },
    "connect_timeout": 10000,
}


def _new_aerospike_client(config: Dict[str, Any]) -> aerospike.Client:
    return aerospike.client(config).connect()


class AerospikeProductStoreScenario(ProductStoreScenarioImpl):
    NS = 'test'
    SET = 'products'

    def __init__(self, config: Dict[str, Any]):
        tup = lambda x: (x[0], int(x[1]))
        hosts = [tup(hp.split(":")) for hp in config['hosts']]
        conf = _DEFAULT_CONF.copy()
        conf['hosts'] = hosts
        self.client: aerospike.Client = _new_aerospike_client(conf)

    def clean(self):
        # Setting nanos=0 will delete all entries in the set
        self.client.truncate(self.NS, self.SET, nanos=0)

    def load_products(self, products: Sequence[Product]) -> None:
        for product in products:
            key = (self.NS, self.SET, product.product_id)
            self.client.put(key, asdict(product))

    def get_product_title(self, product_id: str) -> str:
        key = (self.NS, self.SET, product_id)
        key2, meta, bins = self.client.get(key)
        return bins['title']

    def get_product_desc(self, product_id: str) -> str:
        key = (self.NS, self.SET, product_id)
        key2, meta, bins = self.client.get(key)
        return bins['description']
