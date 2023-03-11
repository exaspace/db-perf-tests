from dataclasses import asdict
from typing import Any, Dict, Sequence

from pymongo import MongoClient

from scenarios import Product, ProductStoreScenarioImpl


def _new_client(config: Dict[str, Any]) -> MongoClient:
    client = MongoClient(config['url'])
    return client


class MongoProductStoreScenario(ProductStoreScenarioImpl):
    DB_NAME = 'test'
    COLLECTION = 'products'

    def __init__(self, config: Dict[str, Any]):
        self.client = _new_client(config)
        self.db = self.client[self.DB_NAME]

    def clean(self) -> None:
        self.db[self.COLLECTION].drop()

    def load_products(self, products: Sequence[Product]) -> None:
        self.db[self.COLLECTION].insert_many([{**asdict(p), '_id': p.product_id} for p in products])

    def load_products_naive(self, products: Sequence[Product]) -> None:
        # WARNING: this will be far slower than using insert_many()
        for product in products:
            self.db[self.COLLECTION].insert_one({**asdict(product), '_id': product.product_id})

    def get_product_title(self, product_id: str) -> str:
        res = self.db[self.COLLECTION].find_one({'_id': product_id}, {'title': 1, '_id': 0})
        return res['title']

    def get_product_desc(self, product_id: str) -> str:
        res = self.db[self.COLLECTION].find_one({'_id': product_id}, {'description': 1, '_id': 0})
        return res['description']
