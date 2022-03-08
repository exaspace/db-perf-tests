

* https://aerospike-python-client.readthedocs.io/en/latest/client.html


Useful Aerospike commands

    aql> show sets
    aql> select * from test.products where PK = '28ef2c54-0c1f-4c1c-85df-a240010ee26a';

    asinfo -v 'sets/test/products'
    asinfo -v 'histogram:type=object-size;namespace=test'


Useful Redis commands

    redis-cli HGETALL product:6058ac0c-9320-4224-b259-02bd756cd59f


Running services

    docker run --rm -d --name aerospike -p 3000-3002:3000-3002 aerospike:ce-5.7.0.10    
    docker run --rm -d --name mongo -p 27017:27017 mongo    
    docker run --rm -d --name postgres -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust postgres
    docker run --rm -d --name redis -p 6379:6379 redis

Testing 

Download data.csv.zip from https://www.kaggle.com/carrie1/ecommerce-data

