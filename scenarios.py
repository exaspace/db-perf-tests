import random

from exaspace_datagen import EcommerceGenerator
from clock import Timer


class ProductStoreScenario:

    def __init__(self, num_products, num_queries):
        self.num_queries = num_queries
        ecom = EcommerceGenerator(num_products)
        self.products = list(ecom.gen_products())

    def _check_products_stored_correctly(self, impl):
        test_products = [random.choice(self.products) for _ in range(3)]
        for p in test_products:
            title = impl.get_product_title(p['product_id'])
            desc = impl.get_product_desc(p['product_id'])
            assert title == p['title'], f"{title} {p['title']}"
            assert desc == p['description']

    def execute(self, impl):
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
