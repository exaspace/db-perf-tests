import aerospike_scenarios
import postgres_scenarios
import redis_scenarios
from aerospike_scenarios import AerospikeProductStoreScenario
from redis_scenarios import RedisProductStoreScenarioUsingHashes
from postgres_scenarios import PostgresProductStoreScenario

if __name__ == "__main__":

    sizes = [(100, 100), (1_000, 4_000), (10_000, 40_000)]

    size_choice = 0
    run = [
        'aerospike',
        'redis',
        'postgres',
    ]

    np = sizes[size_choice][0]
    nq = sizes[size_choice][1]

    if 'postgres' in run:
        PostgresProductStoreScenario(postgres_scenarios.LOCALHOST, num_products=np, num_queries=nq).execute()

    if 'redis' in run:
        RedisProductStoreScenarioUsingHashes(redis_scenarios.LOCALHOST, num_products=np, num_queries=nq).execute()

    if 'aerospike' in run:
        AerospikeProductStoreScenario(aerospike_scenarios.LOCALHOST, num_products=np, num_queries=nq).execute()
