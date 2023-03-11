import argparse

import yaml

from aerospike_scenarios import AerospikeProductStoreScenario
from mongo_scenarios import MongoProductStoreScenario
from postgres_scenarios import PostgresProductStoreScenario, PostgresProductStoreScenarioJson
from redis_scenarios import RedisProductStoreScenarioUsingHashes
from scenarios import ProductStoreScenario

SIZE_ARGS = ["small", "medium", "large"]

SCENARIOS = {
    "product_store": {
        "main_class": ProductStoreScenario,
        "implementations": {
            "aerospike": AerospikeProductStoreScenario,
            "postgres": PostgresProductStoreScenario,
            "postgres_json": PostgresProductStoreScenarioJson,
            "mongo": MongoProductStoreScenario,
            "yugabyte": PostgresProductStoreScenario,
            "yugabyte_json": PostgresProductStoreScenarioJson,
            "redis": RedisProductStoreScenarioUsingHashes,
            "cockroach": PostgresProductStoreScenario,
            "cockroach_json": PostgresProductStoreScenarioJson
        },
        "sizes": {
            "small": {
                "num_products": 200, "num_queries": 200
            },
            "medium": {
                "num_products": 1_000, "num_queries": 2_000
            },
            "large": {
                "num_products": 10_000, "num_queries": 20_000
            },
        }
    }
}


def read_config():
    with open("config.yml") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def main():
    all_configs = read_config()

    parser = argparse.ArgumentParser(description='database perf test tool')
    parser.add_argument('-s', '--scenario',
                        metavar='scenario',
                        type=str,
                        help='Scenario name (e.g. "product_store")')
    parser.add_argument('-i', '--impl',
                        metavar='implementation',
                        type=str,
                        help='Implementation name (e.g. "postgres", "postgres_json")')
    parser.add_argument('-c', '--connection',
                        type=str,
                        help=f'Connection name as set in the configuration file')
    parser.add_argument('--size',
                        type=str,
                        default="small",
                        help=f'Size of test')
    parser.add_argument('--list',
                        action='store_true',
                        help=f'List scenarios')
    args = parser.parse_args()

    if args.list:
        print(", ".join(SCENARIOS.keys()))
        exit(0)

    if args.scenario not in SCENARIOS:
        avail = set(SCENARIOS.keys())
        parser.error(f"Unknown scenario '{args.scenario}'. Available: {avail}")

    scenario_definition = SCENARIOS[args.scenario]

    if args.size not in scenario_definition["sizes"]:
        avail = set(scenario_definition['sizes'].keys())
        parser.error(f"Unknown size '{args.size}'. Available: {avail}")

    size = scenario_definition["sizes"][args.size]

    if args.impl not in scenario_definition["implementations"]:
        avail = set(scenario_definition["implementations"])
        parser.error(f"Unknown implementation '{args.impl}'. Available: {avail}")

    impl_class = scenario_definition["implementations"][args.impl]

    if args.connection not in all_configs:
        avail = set(all_configs.keys())
        parser.error(f"Connection {args.connection} not defined in config file. Available: {avail}")

    main_class = scenario_definition['main_class']
    scenario = main_class(size=size)
    impl_config = all_configs[args.connection]
    _timer = scenario.execute(impl_class(impl_config))


if __name__ == "__main__":
    main()
