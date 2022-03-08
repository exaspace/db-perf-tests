import psycopg2
from psycopg2.extras import execute_values
from scenarios import ProductStoreScenario

LOCALHOST = {
    'dbname': 'postgres',
    'user': 'postgres',
    'host': 'localhost',
    'password': ' ',
}


def new_postgres_client(config):
    return psycopg2.connect(
        f"host={config['host']} dbname={config['dbname']} user={config['user']} password={config['password']}")


class PostgresProductStoreScenario:
    CREATE_SQL = """
        DROP TABLE IF EXISTS products;
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

    INSERT_SQL_1 = """
    INSERT INTO products (product_id, created_ts, title, description, url, price) 
    VALUES (%(product_id)s, %(created_ts)s, %(title)s, %(description)s, %(url)s, %(price)s)
    """

    def __init__(self, config, num_products, num_queries):
        self.conn = new_postgres_client(config)
        self.scenario = ProductStoreScenario(num_products, num_queries)

    def _clean_create(self):
        curs = self.conn.cursor()
        curs.execute(self.CREATE_SQL)
        self.conn.commit()
        curs.close()

    def execute(self):
        self._clean_create()
        self.scenario.execute(self)

    def load_products(self, products):
        curs = self.conn.cursor()
        seq = [(p['product_id'], p['created_ts'], p['title'], p['description'], p['url'], p['price'])
               for p in products]
        execute_values(curs, self.INSERT_SQL, seq)
        self.conn.commit()
        curs.close()

    def load_products_naive(self, products):
        # WARNING: this will be far slower than using execute_values()
        curs = self.conn.cursor()
        for i, product in enumerate(products):
            curs.execute(self.INSERT_SQL_1, product)
            if i % 1000 == 0:
                self.conn.commit()
        self.conn.commit()
        curs.close()

    def get_product_title(self, product_id):
        with self.conn.cursor() as curs:
            curs.execute('SELECT title FROM products WHERE product_id = %s', (product_id,))
            return curs.fetchone()[0]

    def get_product_desc(self, product_id):
        with self.conn.cursor() as curs:
            curs.execute('SELECT description FROM products WHERE product_id = %s', (product_id,))
            return curs.fetchone()[0]
