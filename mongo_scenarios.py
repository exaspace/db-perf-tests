from typing import Any, Dict

from pymongo import MongoClient

from scenarios import ProductStoreScenario

LOCALHOST = {
    'url': 'localhost:27017'
}


def new_client(config: Dict[str, Any]) -> MongoClient:
    client = MongoClient(config['url'])
    return client


class MongoProductStoreScenario:

    DB_NAME = 'test'
    COLLECTION = 'products'

    def __init__(self, config, num_products, num_queries):
        self.client = new_client(config)
        self.db = self.client[self.DB_NAME]
        self.scenario = ProductStoreScenario(num_products, num_queries)

    def execute(self):
        self.db[self.COLLECTION].drop()
        self.scenario.execute(self)

    def load_products(self, products):
        self.db[self.COLLECTION].insert_many([{**p, '_id': p['product_id']} for p in products])

    def load_products_naive(self, products):
        # WARNING: this will be far slower than using insert_many()
        for product in products:
            self.db[self.COLLECTION].insert_one({**product, '_id': product['product_id']})

    def get_product_title(self, product_id):
        res = self.db[self.COLLECTION].find_one({'_id': product_id}, {'title': 1, '_id': 0})
        return res['title']

    def get_product_desc(self, product_id):
        res = self.db[self.COLLECTION].find_one({'_id': product_id}, {'description': 1, '_id': 0})
        return res['description']
