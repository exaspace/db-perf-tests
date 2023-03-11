import aerospike_scenarios
import mongo_scenarios
import postgres_scenarios
import redis_scenarios
from aerospike_scenarios import AerospikeProductStoreScenario
from mongo_scenarios import MongoProductStoreScenario
from postgres_scenarios import PostgresProductStoreScenario, PostgresProductStoreScenarioJson
from redis_scenarios import RedisProductStoreScenarioUsingHashes

if __name__ == "__main__":

    sizes = [(200, 200), (1_000, 2_000), (10_000, 20_000)]

    size_choice = 2
    run = [
        'aerospike',
        'cockroach',
        'cockroach_json',
        'mongo',
        'postgres',
        'postgres_json',
        'redis',
        'yugabyte',
        'yugabyte_json',
    ]

    num_products = sizes[size_choice][0]
    num_queries = sizes[size_choice][1]

    print(f"num products: {num_products} num_queries: {num_queries}")

    if 'aerospike' in run:
        AerospikeProductStoreScenario(aerospike_scenarios.LOCALHOST, num_products=num_products, num_queries=num_queries).execute()

    if 'cockroach' in run:
        PostgresProductStoreScenario(postgres_scenarios.LOCALHOST_COCKROACH, num_products=num_products, num_queries=num_queries).execute()

    if 'cockroach_json' in run:
        PostgresProductStoreScenarioJson(postgres_scenarios.LOCALHOST_COCKROACH, num_products=num_products, num_queries=num_queries).execute()

    if 'mongo' in run:
        MongoProductStoreScenario(mongo_scenarios.LOCALHOST, num_products=num_products, num_queries=num_queries).execute()

    if 'postgres' in run:
        PostgresProductStoreScenario(postgres_scenarios.LOCALHOST, num_products=num_products, num_queries=num_queries).execute()

    if 'postgres_json' in run:
        PostgresProductStoreScenarioJson(postgres_scenarios.LOCALHOST, num_products=num_products, num_queries=num_queries).execute()

    if 'redis' in run:
        RedisProductStoreScenarioUsingHashes(redis_scenarios.LOCALHOST, num_products=num_products, num_queries=num_queries).execute()

    if 'yugabyte' in run:
        PostgresProductStoreScenario(postgres_scenarios.LOCALHOST_YUGABYTE, num_products=num_products, num_queries=num_queries).execute()

    if 'yugabyte_json' in run:
        PostgresProductStoreScenarioJson(postgres_scenarios.LOCALHOST_YUGABYTE, num_products=num_products, num_queries=num_queries).execute()

