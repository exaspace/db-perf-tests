import random
import time

from faker import Faker
from clock import Timer


class EcommerceGenerator:
    ONE_YEAR_MS = 365 * 86400 * 1000

    def __init__(self):
        self.fake = Faker()
        Faker.seed(1)
        self.to_ts = self.current_time_ms()
        self.from_ts = self.to_ts - self.ONE_YEAR_MS

    @staticmethod
    def current_time_ms() -> int:
        return int(time.time() * 1000)

    def gen_products(self, count: int, start_id: int = 1):
        for pid in range(start_id, start_id + count):
            yield self._new_product(str(pid))

    def _new_product(self, product_id: str):
        return {
            'product_id': product_id,
            'created_ts': random.randint(self.from_ts, self.to_ts),
            'title': self.fake.paragraph(1),
            'description': self.fake.paragraph(20),
            'url': f'https://someshop.com/product/{product_id}',
            'price': random.randint(0, 1000) + 99,
        }


class ProductStoreScenario:
    """
    Calls load_products() to load test product data
    Calls get_product_title() repeatedly on random product IDs
    Calls get_product_desc() repeatedly on random product IDs
    """
    MAX_NUM_PRODUCTS = 1_000_000

    def __init__(self, num_products: int, num_queries: int):
        assert num_products < self.MAX_NUM_PRODUCTS, \
            '''
            Use smaller number of products as this scenario stores all products in memory before 
            passing them to the implementation's load_products function.
            '''
        self.num_queries = num_queries
        ecom = EcommerceGenerator()
        self.products = list(ecom.gen_products(num_products))

    def _check_products_stored_correctly(self, impl, num_to_check: int = 3):
        test_products = [random.choice(self.products) for _ in range(num_to_check)]
        for p in test_products:
            title = impl.get_product_title(p['product_id'])
            desc = impl.get_product_desc(p['product_id'])
            assert title == p['title'], f"{title} {p['title']}"
            assert desc == p['description']

    def execute(self, impl) -> Timer:
        timer = Timer(type(impl).__name__)
        timer.start_phase("load_products")
        impl.load_products(self.products)
        timer.stop_phase(len(self.products))

        self._check_products_stored_correctly(impl)

        timer.start_phase("query_titles_by_product_id")
        for _ in range(self.num_queries):
            p = random.choice(self.products)
            impl.get_product_title(p['product_id'])
        timer.stop_phase(self.num_queries)

        timer.start_phase("query_descriptions_by_product_id")
        for _ in range(self.num_queries):
            p = random.choice(self.products)
            impl.get_product_desc(p['product_id'])
        timer.stop_phase(self.num_queries)
        return timer
