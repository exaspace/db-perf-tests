import json
from dataclasses import asdict
from typing import Dict, Any, Sequence

import psycopg2
from psycopg2.extras import execute_values

from scenarios import ProductStoreScenarioImpl, Product


def _new_postgres_client(config):
    return psycopg2.connect(
        f"host={config['host']} port={config['port']} dbname={config['dbname']}" +
        f" user={config['user']} password={config['password']}")


class PostgresProductStoreScenario(ProductStoreScenarioImpl):
    DROP_SQL = """
        DROP TABLE IF EXISTS products;"""

    CREATE_SQL = """
        CREATE TABLE products (
            product_id VARCHAR(44) PRIMARY KEY NOT NULL, 
            created_ts BIGINT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            url TEXT NOT NULL,
            price NUMERIC NOT NULL
        )
        """

    INSERT_SQL = """
    INSERT INTO products (product_id, created_ts, title, description, url, price) 
    VALUES %s
    """

    INSERT_SQL_NAIVE = """
    INSERT INTO products (product_id, created_ts, title, description, url, price) 
    VALUES (%(product_id)s, %(created_ts)s, %(title)s, %(description)s, %(url)s, %(price)s)
    """

    QUERY_TITLE = """
    SELECT title FROM products WHERE product_id = %s
    """

    QUERY_DESC = """
    SELECT description FROM products WHERE product_id = %s
    """

    def __init__(self, config: Dict[str, Any]):
        self.conn = _new_postgres_client(config)

    def clean(self) -> None:
        curs = self.conn.cursor()
        curs.execute(self.DROP_SQL)
        self.conn.commit()
        curs.execute(self.CREATE_SQL)
        self.conn.commit()
        curs.close()

    def load_products(self, products: Sequence[Product]) -> None:
        curs = self.conn.cursor()
        # WARNING: builds large sequence in memory
        seq = [(p.product_id, p.created_ts, p.title, p.description, p.url, p.price)
               for p in products]
        execute_values(curs, self.INSERT_SQL, seq)
        self.conn.commit()
        curs.close()

    def load_products_naive(self, products: Sequence[Product]) -> None:
        # WARNING: this will be far slower than using execute_values()
        curs = self.conn.cursor()
        for i, product in enumerate(products):
            curs.execute(self.INSERT_SQL_NAIVE, product)
            if i % 1000 == 0:
                self.conn.commit()
        self.conn.commit()
        curs.close()

    def get_product_title(self, product_id: str) -> str:
        with self.conn.cursor() as curs:
            curs.execute(self.QUERY_TITLE, (product_id,))
            return curs.fetchone()[0]

    def get_product_desc(self, product_id: str) -> str:
        with self.conn.cursor() as curs:
            curs.execute(self.QUERY_DESC, (product_id,))
            return curs.fetchone()[0]


class PostgresProductStoreScenarioJson(ProductStoreScenarioImpl):
    DROP_SQL = """
        DROP TABLE IF EXISTS products_json;"""

    CREATE_SQL = """
        CREATE TABLE products_json (
            doc JSONB NOT NULL 
        )
        """

    CREATE_INDEX_SQL = """
        CREATE INDEX products_json_idx ON products_json USING GIN(doc)
        """

    INSERT_SQL = """
    INSERT INTO products_json (doc) 
    VALUES %s
    """

    def __init__(self, config: Dict[str, Any]):
        self.conn = _new_postgres_client(config)

    def clean(self) -> None:
        with self.conn.cursor() as curs:
            curs.execute(self.DROP_SQL)
            self.conn.commit()
            curs.execute(self.CREATE_SQL)
            self.conn.commit()
            curs.execute(self.CREATE_INDEX_SQL)
            self.conn.commit()

    def load_products(self, products: Sequence[Product]) -> None:
        with self.conn.cursor() as curs:
            seq = [(json.dumps(asdict(p)),) for p in products]
            execute_values(curs, self.INSERT_SQL, seq)
            self.conn.commit()

    def get_product_title(self, product_id: str) -> str:
        with self.conn.cursor() as curs:
            curs.execute('SELECT doc->>\'title\' FROM products_json WHERE doc->>\'product_id\' = %s',
                         (product_id,))
            return curs.fetchone()[0]

    def get_product_desc(self, product_id: str) -> str:
        with self.conn.cursor() as curs:
            curs.execute('SELECT doc->>\'description\' FROM products_json WHERE doc->>\'product_id\' = %s',
                         (product_id,))
            return curs.fetchone()[0]
