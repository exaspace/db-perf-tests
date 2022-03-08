import redis

from scenarios import ProductStoreScenario

LOCALHOST = {
    'host': 'localhost',
    "port": 6379,
    "db": 0,
}


def new_redis_client(config):
    return redis.Redis(host=config['host'], port=config['port'], db=config['db'])


def to_utf8(bytes):
    if bytes is not None:
        return bytes.decode('utf-8')
    return None


class RedisProductStoreScenarioUsingHashes:

    def __init__(self, config, num_products, num_queries):
        self.client = new_redis_client(config)
        self.scenario = ProductStoreScenario(num_products, num_queries)

    def execute(self):
        self._clean()
        self.scenario.execute(self)

    def _clean(self):
        self.client.flushdb()

    def load_products(self, products):
        for product in products:
            product_id = product['product_id']
            self.client.hset(f"product:{product_id}", mapping=product)

    def get_product_title(self, product_id):
        return to_utf8(self.client.hget(f"product:{product_id}", 'title'))

    def get_product_desc(self, product_id):
        return to_utf8(self.client.hget(f"product:{product_id}", 'description'))
