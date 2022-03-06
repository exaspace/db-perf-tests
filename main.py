import aerospike_scenarios
import redis_scenarios
from aerospike_scenarios import AerospikeProductStoreScenario
from redis_scenarios import RedisProductStoreScenarioUsingSimpleKV, RedisProductStoreScenarioUsingHashes

if __name__ == "__main__":
    RedisProductStoreScenarioUsingSimpleKV(redis_scenarios.LOCALHOST, num_products=1000, num_queries=1000).execute()
    RedisProductStoreScenarioUsingHashes(redis_scenarios.LOCALHOST, num_products=1000, num_queries=1000).execute()
    AerospikeProductStoreScenario(aerospike_scenarios.LOCALHOST, num_products=1000, num_queries=1000).execute()
