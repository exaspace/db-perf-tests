import aerospike

from scenarios import ProductStoreScenario

LOCALHOST = {
    'hosts': [('127.0.0.1', 3000)],
    "policies": {
        "login_timeout_ms": 10000
    },
    "connect_timeout": 10000,
}


def new_aerospike_client(config):
    return aerospike.client(config).connect()


class AerospikeProductStoreScenario:

    def __init__(self, config, num_products, num_queries):
        self.client = new_aerospike_client(config)
        self.scenario = ProductStoreScenario(num_products, num_queries)

    def execute(self):
        self.scenario.execute(self)

    def load_products(self, products):
        for product in products:
            key = ('test', 'products', product['product_id'])
            value = {
                'title': product['title'],
                'description': product['description'],
            }
            self.client.put(key, value)

    def get_product_title(self, product_id):
        key = ('test', 'products', product_id)
        key2, meta, bins = self.client.get(key)
        return bins['title']

    def get_product_desc(self, product_id):
        key = ('test', 'products', product_id)
        key2, meta, bins = self.client.get(key)
        return bins['description']


if __name__ == "__main__":
    AerospikeProductStoreScenario(LOCALHOST, num_products=1000, num_queries=5000).execute()
