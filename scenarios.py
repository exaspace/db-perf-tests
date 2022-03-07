import random

from exaspace_datagen import EcommerceGenerator
from clock import Timer


class ProductStoreScenario:
    MAX_NUM_PRODUCTS = 1_000_000

    def __init__(self, num_products, num_queries):
        assert num_products < self.MAX_NUM_PRODUCTS, \
            '''
            Use smaller number of products as this scenario stores all products in memory before 
            passing them to the implementation's load_products function.
            '''

        self.num_queries = num_queries
        ecom = EcommerceGenerator()
        self.products = list(ecom.gen_products(num_products))
        p = self.products[0]
        print(f"Generated {num_products} products (example: {p['product_id']} '{p['title']}')")

    def _check_products_stored_correctly(self, impl, num_to_check=3):
        test_products = [random.choice(self.products) for _ in range(num_to_check)]
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
