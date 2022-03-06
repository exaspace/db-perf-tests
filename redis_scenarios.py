import redis

from scenarios import ProductStoreScenario

LOCALHOST = {
    'host': 'localhost',
    "port": 6379,
    "db": 0,
}


def new_redis_client(config):
    return redis.Redis(host=config['host'], port=config['port'], db=config['db'])


def utf8(bytes):
    if bytes is not None:
        return bytes.decode('utf-8')
    return None


class RedisProductStoreScenarioUsingHashes:

    def __init__(self, config, num_products, num_queries):
        self.client = new_redis_client(config)
        self.scenario = ProductStoreScenario(num_products, num_queries)

    def execute(self):
        self.scenario.execute(self)

    def load_products(self, products):
        for product in products:
            value = {
                'title': product['title'],
                'description': product['description'],
            }
            product_id = product['product_id']
            self.client.hset(f"product:{product_id}", mapping=value)
            # self.client.set(f"title.{product_id}", p['title'])
            # self.client.set(f"description.{product_id}", p['description'])

    def get_product_title(self, product_id):
        return utf8(self.client.hget(f"product:{product_id}", 'title'))

    def get_product_desc(self, product_id):
        return utf8(self.client.hget(f"product:{product_id}", 'description'))


class RedisProductStoreScenarioUsingSimpleKV:

    def __init__(self, config, num_products, num_queries):
        self.client = new_redis_client(config)
        self.scenario = ProductStoreScenario(num_products, num_queries)

    def execute(self):
        self.scenario.execute(self)

    def load_products(self, products):
        for product in products:
            product_id = product['product_id']
            self.client.set(f"title.{product_id}", product['title'])
            self.client.set(f"description.{product_id}", product['description'])

    def get_product_title(self, product_id):
        return utf8(self.client.get(f"title.{product_id}"))

    def get_product_desc(self, product_id):
        return utf8(self.client.get(f"description.{product_id}"))


if __name__ == "__main__":
    RedisProductStoreScenarioUsingSimpleKV(LOCALHOST, num_products=10, num_queries=100).execute()
    RedisProductStoreScenarioUsingHashes(LOCALHOST, num_products=10, num_queries=100).execute()
