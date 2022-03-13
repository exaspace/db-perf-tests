# General Resources

* https://aerospike-python-client.readthedocs.io/en/latest/client.html
* https://github.com/cmu-db/benchbase/tree/main/docker/tpch
* https://www.perfectlyrandom.org/2019/11/29/handling-avro-files-in-python/
* https://escholarship.org/content/qt6z39j27q/qt6z39j27q.pdf?t=oeir6c



# Useful Commands / Info

Aerospike 

    aql> show sets
    aql> select * from test.products where PK = '28ef2c54-0c1f-4c1c-85df-a240010ee26a';

    asinfo -v 'sets/test/products'
    asinfo -v 'histogram:type=object-size;namespace=test'


Redis

    redis-cli HGETALL product:6058ac0c-9320-4224-b259-02bd756cd59f



# Running services in Docker

Run via the included docker-compose.

Or to run manually:

    docker run --rm -d --name aerospike -p 3000-3002:3000-3002 aerospike:ce-5.7.0.10    
    docker run --rm -d --name cockroach -p 26257:26257 -p 8080:8080 cockroachdb/cockroach:v21.2.6 start-single-node --insecure
    docker run --rm -d --name mongo -p 27017:27017 mongo    
    docker run --rm -d --name postgres -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust postgres
    docker run --rm -d --name redis -p 6379:6379 redis

Testing 

Download data.csv.zip from https://www.kaggle.com/carrie1/ecommerce-data

