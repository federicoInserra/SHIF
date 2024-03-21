// indexes = {
//     "docs_chunks":{
//         "searchIndex":{
//             "name":"searchIndex",
//             "type":"search",
//             "definition":{
//                 "mappings": {
//                     "dynamic": false,
//                     "fields": {
//                         "published": [
//                             {
//                             "type": "date"
//                             },
//                             {
//                             "type": "dateFacet"
//                             }
//                         ],
//                         "authors": [
//                             {
//                             "type": "string"
//                             },
//                             {
//                             "type": "token"
//                             },
//                             {
//                             "type": "stringFacet"
//                             }
//                         ],
//                         "parent_link": [
//                             {
//                             "type": "string"
//                             },
//                             {
//                             "type": "token"
//                             },
//                             {
//                             "type": "stringFacet"
//                             }
//                         ],
//                         "tags": [
//                             {
//                             "type": "string"
//                             },
//                             {
//                             "type": "token"
//                             },
//                             {
//                             "type": "stringFacet"
//                             }
//                         ],
//                         "nasdaq_tickers": [
//                             {
//                             "type": "string"
//                             },
//                             {
//                             "type": "token"
//                             },
//                             {
//                             "type": "stringFacet"
//                             }
//                         ],
//                         "content": {
//                             "type":"string"
//                         }
                    
//                     }
//                 }
//                 }
//         },
//         "vectorIndex":{
//             "name":"vectorIndex",
//             "type":"vectorSearch",
//             "definition":{
//                 "fields":[
//                     {
//                         "type": "vector",
//                         "path": "embedding",
//                         "numDimensions": 1536,
//                         "similarity": "cosine"
//                     },
//                     {
//                         "type":"filter",
//                         "path":"published",
//                     },
//                     {
//                         "type":"filter",
//                         "path":"type",
//                     }
//                     ,
//                     {
//                         "type":"filter",
//                         "path":"nasdaq_tickers",
//                     }
//                 ]
//             }
//         }
//     },
//     "funds_chunks":{
//         "searchIndex":{
//             "name":"searchIndex",
//             "type":"search",
//             "definition":{
//                 "mappings": {
//                     "dynamic": true,
//                 }
//             }
//         },
//         "vectorIndex":{
//             "name":"vectorIndex",
//             "type":"vectorSearch",
//             "definition":{
//                 "fields": [
//                     {
//                         "type": "vector",
//                         "path": "embedding",
//                         "numDimensions": 1536,
//                         "similarity": "cosine"
//                     }
//                 ]
//             }
//         }
//     }
// };

db = db.getSiblingDB("shif");

db.runCommand(
    {
        createSearchIndexes: "docs_chunks",
        indexes:[
            {
                "name":"searchIndex",
                "type":"search",
                "definition":{
                    "mappings": {
                        "dynamic": false,
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
            },
            {
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
        ]
    }
)
db.runCommand(
    {
        createSearchIndexes: "funds_chunks",
        indexes:[
            {
                "name":"searchIndex",
                "type":"search",
                "definition":{
                    "mappings": {
                        "dynamic": true,
                    }
                }
            },
            {
                "name":"vectorIndex",
                "type":"vectorSearch",
                "definition":{
                    "fields": [
                        {
                            "type": "vector",
                            "path": "embedding",
                            "numDimensions": 1536,
                            "similarity": "cosine"
                        }
                    ]
                }
            }
        ]
    }
)

