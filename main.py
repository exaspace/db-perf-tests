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

    size_choice = 1
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

    np = sizes[size_choice][0]
    nq = sizes[size_choice][1]

    if 'aerospike' in run:
        AerospikeProductStoreScenario(aerospike_scenarios.LOCALHOST, num_products=np, num_queries=nq).execute()

    if 'cockroach' in run:
        PostgresProductStoreScenario(postgres_scenarios.LOCALHOST_COCKROACH, num_products=np, num_queries=nq).execute()

    if 'cockroach_json' in run:
        PostgresProductStoreScenarioJson(postgres_scenarios.LOCALHOST_COCKROACH, num_products=np, num_queries=nq).execute()

    if 'mongo' in run:
        MongoProductStoreScenario(mongo_scenarios.LOCALHOST, num_products=np, num_queries=nq).execute()

    if 'postgres' in run:
        PostgresProductStoreScenario(postgres_scenarios.LOCALHOST, num_products=np, num_queries=nq).execute()

    if 'postgres_json' in run:
        PostgresProductStoreScenarioJson(postgres_scenarios.LOCALHOST, num_products=np, num_queries=nq).execute()

    if 'redis' in run:
        RedisProductStoreScenarioUsingHashes(redis_scenarios.LOCALHOST, num_products=np, num_queries=nq).execute()

    if 'yugabyte' in run:
        PostgresProductStoreScenario(postgres_scenarios.LOCALHOST_YUGABYTE, num_products=np, num_queries=nq).execute()

    if 'yugabyte_json' in run:
        PostgresProductStoreScenarioJson(postgres_scenarios.LOCALHOST_YUGABYTE, num_products=np, num_queries=nq).execute()

