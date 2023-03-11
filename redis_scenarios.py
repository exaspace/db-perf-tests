from dataclasses import asdict
from typing import Dict, Any, Sequence

import redis

from scenarios import ProductStoreScenarioImpl, Product


def _new_redis_client(config):
    return redis.Redis(host=config['host'], port=config['port'], db=config['db'])


def _to_utf8(bytes):
    if bytes is not None:
        return bytes.decode('utf-8')
    return None


class RedisProductStoreScenarioUsingHashes(ProductStoreScenarioImpl):

    def __init__(self, config: Dict[str, Any]):
        self.client = _new_redis_client(config)

    def clean(self) -> None:
        self.client.flushdb()

    def load_products(self, products: Sequence[Product]) -> None:
        for product in products:
            product_id = product.product_id
            self.client.hset(f"product:{product_id}", mapping=asdict(product))

    def get_product_title(self, product_id: str) -> str:
        return _to_utf8(self.client.hget(f"product:{product_id}", 'title'))

    def get_product_desc(self, product_id: str) -> str:
        return _to_utf8(self.client.hget(f"product:{product_id}", 'description'))
