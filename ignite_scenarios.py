import os
from dataclasses import astuple
from typing import Dict, Any, Sequence

from pyignite import Client
from pyignite.cache import Cache

from scenarios import ProductStoreScenarioImpl, Product


def _new_client(config: Dict[str, Any]):
    client = Client()
    client.connect(config['host'], config['port'])
    return client


def _activate():
    # This is not pretty
    # Better way (but more hassle) would be to build ignite image to activate the REST API
    # And call that to activate.
    print("Activating Ignite...")
    os.system("docker compose exec ignite /opt/ignite/apache-ignite/bin/control.sh --activate")
    print("Done activating Ignite")


class IgniteProductStoreScenarioBasicKV(ProductStoreScenarioImpl):

    def __init__(self, config: Dict[str, Any]):
        _activate()
        self.client = _new_client(config)
        self.cache: Cache = self.client.get_or_create_cache('titles')
        self.cache2: Cache = self.client.get_or_create_cache('descriptions')

    def clean(self) -> None:
        if self.cache.get_size() > 0:
            self.cache.remove_all()
        if self.cache2.get_size() > 0:
            self.cache2.remove_all()

    def load_products(self, products: Sequence[Product]) -> None:
        for product in products:
            product_id = product.product_id
            self.cache.put(product_id, product.title)
            self.cache2.put(product_id, product.description)

    def get_product_title(self, product_id: str) -> str:
        return self.cache.get(product_id)

    def get_product_desc(self, product_id: str) -> str:
        return self.cache2.get(product_id)


class IgniteProductStoreScenarioSQL(ProductStoreScenarioImpl):
    DROP_TABLE_QUERY = """
    DROP TABLE IF EXISTS products"""

    CREATE_TABLE_QUERY = """
    CREATE TABLE products (
        product_id CHAR(12),
        created_ts BIGINT,
        title CHAR(128),
        description CHAR(2048),
        url CHAR(512),
        price INT(11),
       
        PRIMARY KEY (product_id)
    )"""

    INSERT_PRODUCT_QUERY = """
    INSERT INTO products (product_id, created_ts, title, description, url, price) 
    VALUES (?, ?, ?, ?, ?, ?,)
    """

    QUERY_TITLE = """
    SELECT title FROM products WHERE product_id = ?
    """

    QUERY_DESC = """
    SELECT description FROM products WHERE product_id = ?
    """

    DELETE_QUERY = """
    DELETE FROM products
    """

    def __init__(self, config: Dict[str, Any]):
        _activate()
        self.client = _new_client(config)
        self.client.sql(self.DROP_TABLE_QUERY)
        self.client.sql(self.CREATE_TABLE_QUERY)

    def clean(self) -> None:
        self.client.sql(self.DELETE_QUERY)

    def load_products(self, products: Sequence[Product]) -> None:
        for p in products:
            self.client.sql(self.INSERT_PRODUCT_QUERY, query_args=astuple(p))

    def get_product_title(self, product_id: str) -> str:
        return next(self.client.sql(self.QUERY_TITLE, query_args=[product_id]))[0]

    def get_product_desc(self, product_id: str) -> str:
        return next(self.client.sql(self.QUERY_DESC, query_args=[product_id]))[0]
