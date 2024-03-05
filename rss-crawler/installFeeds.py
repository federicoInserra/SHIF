from feeds import feeds
from crawler import MongoDBConnection

connection=MongoDBConnection()
db=connection.connect()

installed = list(db["feeds"].find())
if len(installed) < 1:
    db['feeds'].insert_many(feeds)
    print("Installed all feeds: {}".format(", ".join([feed["_id"] for feed in feeds])))
else:
    for feed in feeds:
        print("Processing feed {}".format(feed['_id']))
        if feed['_id'] in [item['_id'] for item in installed]:
            print("\tFeed is already installed") 
        else:
            print("\tAdding config for feed.")
            db['feeds'].insert_one(feed)
connection.close()