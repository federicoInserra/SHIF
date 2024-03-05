from crawler import MongoDBConnection
from pymongo.errors import CollectionInvalid,OperationFailure

connection=MongoDBConnection()
db=connection.connect()

for c in ["feeds","queue","logs","docs","docs_chunks"]:
    try:
        db.create_collection(c,check_exists=True)
    except CollectionInvalid as e:
        print("The {} collection already exists:".format(c), e)
        pass

feeds_search_index = {
    "name":"default",
    "definition":{
        "mappings": {
            "dynamic": False,
            "fields": {
                "_id": {
                    "type": "autocomplete"
                },
                "config":{
                    "type": "document",
                    "fields": {
                        "attribution":{
                            "type": "autocomplete"
                        },
                        'url':{
                            "type": "autocomplete",
                            "tokenization":"nGram",
                            "minGrams":3,
                            "maxGrams":20
                        }
                    }
                }
            }
        }
    }
}

docs_search_index = {
    "name":"searchIndex",
    "definition":{
        "mappings": {
            "dynamic": False,
            "fields": {
            "published": [
                {
                "type": "date"
                },
                {
                "type": "dateFacet"
                }
            ],
            "attribution": [
                {
                "type": "string"
                },
                {
                "type": "token"
                },
                {
                "type": "stringFacet"
                }
            ],
            "authors": [
                {
                "type": "string"
                },
                {
                "type": "token"
                },
                {
                "type": "stringFacet"
                }
            ],
            "lang": [
                {
                "type": "token"
                },
                {
                "type": "stringFacet"
                }
            ],
            "tags": [
                {
                "type": "string"
                },
                {
                "type": "token"
                },
                {
                "type": "stringFacet"
                }
            ],
            "nasdaq_tickers": [
                {
                "type": "string"
                },
                {
                "type": "token"
                },
                {
                "type": "stringFacet"
                }
            ],
            "summary": {
                "type": "document",
                "fields": {
                "en": {
                    "type": "string",
                    "analyzer": "lucene.english",
                    "searchAnalyzer": "lucene.english"
                },
                "es": {
                    "type": "string",
                    "analyzer": "lucene.spanish",
                    "searchAnalyzer": "lucene.spanish"
                },
                "fr": {
                    "type": "string",
                    "analyzer": "lucene.french",
                    "searchAnalyzer": "lucene.french"
                }
                }
            },
            "content": {
                "type": "document",
                "fields": {
                "en": {
                    "type": "string",
                    "analyzer": "lucene.english",
                    "searchAnalyzer": "lucene.english"
                },
                "es": {
                    "type": "string",
                    "analyzer": "lucene.spanish",
                    "searchAnalyzer": "lucene.spanish"
                },
                "fr": {
                    "type": "string",
                    "analyzer": "lucene.french",
                    "searchAnalyzer": "lucene.french"
                }
                }
            },
            "title": {
                "type": "document",
                "fields": {
                "en": [
                    {
                    "type": "string",
                    "analyzer": "lucene.english",
                    "searchAnalyzer": "lucene.english"
                    },
                    {
                    "type": "autocomplete"
                    }
                ],
                "es": [
                    {
                    "type": "string",
                    "analyzer": "lucene.spanish",
                    "searchAnalyzer": "lucene.spanish"
                    },
                    {
                    "type": "autocomplete"
                    }
                ],
                "fr": [
                    {
                    "type": "string",
                    "analyzer": "lucene.french",
                    "searchAnalyzer": "lucene.french"
                    },
                    {
                    "type": "autocomplete"
                    }
                ]
                }
            }
            }
        }
        }
}

docs_chunks_search_index = {
    "name":"searchIndex",
    "definition":{
        "mappings": {
            "dynamic": False,
            "fields": {
                "published": [
                    {
                    "type": "date"
                    },
                    {
                    "type": "dateFacet"
                    }
                ],
                "authors": [
                    {
                    "type": "string"
                    },
                    {
                    "type": "token"
                    },
                    {
                    "type": "stringFacet"
                    }
                ],
                "parent_link": [
                    {
                    "type": "string"
                    },
                    {
                    "type": "token"
                    },
                    {
                    "type": "stringFacet"
                    }
                ],
                "tags": [
                    {
                    "type": "string"
                    },
                    {
                    "type": "token"
                    },
                    {
                    "type": "stringFacet"
                    }
                ],
                "nasdaq_tickers": [
                    {
                    "type": "string"
                    },
                    {
                    "type": "token"
                    },
                    {
                    "type": "stringFacet"
                    }
                ],
                "content": {
                    "type":"string"
                }
            
            }
        }
        }
}


docs_chunks_vector_index = {
    "name":"vectorIndex",
    "type":"vectorSearch",
    "definition":{
        "fields":[
            {
                "type": "vector",
                "path": "embedding",
                "numDimensions": 1536,
                "similarity": "cosine"
            },
            {
                "type":"filter",
                "path":"published",
            },
            {
                "type":"filter",
                "path":"type",
            }
            ,
            {
                "type":"filter",
                "path":"nasdaq_tickers",
            }
        ]
    }
}

for m in [{'c':"feeds",'m':feeds_search_index},{'c':"docs",'m':docs_search_index},{'c':'docs_chunks','m':docs_chunks_search_index,'v':docs_chunks_vector_index}]:
    print("Creating search index {} for {}".format(m['m']['name'],m['c']))
    try:
        db.get_collection(m['c']).create_search_index(model=m['m'])
    except OperationFailure as e:
        if 'codeName' in e.details and e.details['codeName'] == 'IndexAlreadyExists':
            print("\tIndex already exists")
            pass
        else:
            print("\tError creating index:", e)
            raise e
    if 'v' in m:
        print("Creating vector index {} for {}".format(m['v']['name'],m['c']))
        try:
            db.command("createSearchIndexes",m['c'],indexes=[m['v']])
        except OperationFailure as e:
            if 'codeName' in e.details and e.details['codeName'] == 'IndexAlreadyExists':
                print("\tIndex already exists")
                pass
            else:
                print("\tError creating index:", e)
                raise e
connection.close()