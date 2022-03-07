

Useful Aerospike commands

    aql> show sets
    aql> select * from test.products where PK = '28ef2c54-0c1f-4c1c-85df-a240010ee26a';

    asinfo -v "sets"
    asinfo -v 'histogram:type=object-size;namespace=test'


Useful Redis commands

    redis-cli HGETALL product:6058ac0c-9320-4224-b259-02bd756cd59f


Testing 

Download data.csv.zip from https://www.kaggle.com/carrie1/ecommerce-data

