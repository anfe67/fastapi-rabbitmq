import pprint
from tinydb import Query, TinyDB, where

countries_db = TinyDB("countries.json")

countries_table = countries_db.table(name="countries")
query = Query()
query_def = (query.population > 220_000_000) # & (query.population < 2_250_000_000)

results = countries_table.search(where("population") > 220_000_000)

# results = countries_table.search(query_def)
pprint.pprint(results)

# pprint(countries_table.get(doc_ids=[9, 10]))

print(len(countries_table))

countries_db.close()