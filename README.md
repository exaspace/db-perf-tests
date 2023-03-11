# db-perf-tests

This repo contains a (for the moment very simple) performance test suite for multiple databases. 

Usage:

    python main.py -h

Example:

    python main.py -s product_store -i mongo -c mongo_local --size small 


# Database specific notes

Aerospike 

    aql> show sets
    aql> select * from test.products where PK = '123';

    asinfo -v 'sets/test/products'
    asinfo -v 'histogram:type=object-size;namespace=test'


Redis

    redis-cli HGETALL product:123


# Running the various databases (via Docker)

Run using the included docker compose file 

    docker compose up -d aerospike
    docker compose up -d cockroach
    docker compose up -d mongo
    docker compose up -d postgres
    docker compose up -d redis
    docker compose up -d yugabyte

Or to run directly without compose

    docker run --rm -d --name aerospike -p 3000-3002:3000-3002 aerospike:ce-6.2.0.3    
    docker run --rm -d --name cockroach -p 26257:26257 -p 8080:8080 cockroachdb/cockroach:v22.2.6 \
        start-single-node --insecure
    docker run --rm -d --name mongo -p 27017:27017 mongo:6.0.4    
    docker run --rm -d --name postgres -p 5490:5432 -e POSTGRES_HOST_AUTH_METHOD=trust postgres
    docker run --rm -d --name redis -p 6379:6379 redis
    docker run --rm -d --name yugabyte -p 5433:5433 yugabytedb/yugabyte:2.16.2.0-b41 \
        bin/yugabyted start --daemon=false


# General Resources

* https://aerospike-python-client.readthedocs.io/en/latest/client.html
* https://github.com/cmu-db/benchbase/tree/main/docker/tpch
* https://www.perfectlyrandom.org/2019/11/29/handling-avro-files-in-python/
* https://escholarship.org/content/qt6z39j27q/qt6z39j27q.pdf?t=oeir6c

