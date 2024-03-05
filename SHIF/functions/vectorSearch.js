exports = async function(request,response){
  // This default function will get a value and find a document in MongoDB
  // To see plenty more examples of what you can do with functions see: 
  // https://www.mongodb.com/docs/atlas/app-services/functions/

  // Find the name of the MongoDB service you want to use (see "Linked Data Sources" tab)
  var serviceName = "mongodb-atlas";

  // Update these to reflect your db/collection
  var dbName = "shif";
  
  var collName = request.query.collName;
  var searchIndex = request.query.searchIndex;
  var query = request.query.query;
  var numCandidates = parseInt(request.query.numCandidates);
  var limit = parseInt(request.query.limit);
  var fields = request.query.fields;

  // Get a collection from the context
  var collection = context.services.get(serviceName).db(dbName).collection(collName);
  
  var queryVector = await context.functions.execute("getTextEmbeddingAda",query);
  console.log("Got query vector:");
  console.log(queryVector);
  
  var search = {
    $vectorSearch: {
      index: searchIndex,
      path: 'embedding',
      queryVector:queryVector,
      numCandidates:numCandidates,
      limit:limit
    }
  }
  
  if(request.body){
    // Convert the request body to a JSON string
    const serialized = request.body.text();
    // Parse the string into a usable object
    const body = EJSON.parse(serialized)
    if(body && body.filter && body.filter != ''){
      search.$search.filter=body.filter;
    }
  }
  
  var project = {
    $project:{_id:0}
  }
  
  if(fields && fields != ''){
    fields.split(',').forEach((field)=>{
      project.$project[[field]]=1
    });
  }
  
  var facetStage = 
    {
      $facet:{
        results:[project],
        links: [
          {$group:{_id:"$parent_link",count:{$count:{}}}},
          {$sort:{count:-1}},
          {$limit:25}
        ],
        stock_symbols: [
          {$unwind:{path: "$nasdaq_tickers",preserveNullAndEmptyArrays: false}},
          {$match:{"nasdaq_tickers":{$ne:""}}},
          {$group:{_id:"$nasdaq_tickers",count:{$count:{}}}},
          {$sort:{count:-1}},
          {$limit:25}
        ],
        fund_names:[
          {$group:{_id:"$fund_name",count:{$count:{}}}},
          {$sort:{count:-1}},
          {$limit:limit}
        ],
        sources:[
          {$group:{_id:"$source",count:{$count:{}}}},
          {$sort:{count:-1}},
          {$limit:limit}
        ]
      }
    }
  
  var finalProject = {
    $project:{
      results:1,
      metadata:{
        stock_symbols: {
          $map: {
            input: "$stock_symbols",
            in: "$$this._id"
          }
        },
        links: {
          $map: {
            input: "$links",
            in: "$$this._id"
          }
        },
        fund_names: {
          $map: {
            input: "$fund_names",
            in: "$$this._id"
          }
        },
        sources: {
          $map: {
            input: "$sources",
            in: "$$this._id"
          }
        }
      }
    }
  }
  var pipeline = [search,facetStage,finalProject];
      
  try {
    const r = await collection.aggregate(pipeline).toArray();
    const results = r[0].results;
    const metadata = r[0].metadata;
    response.setStatusCode(200);
    response.setBody(JSON.stringify({results:results,metadata:metadata}));

  } catch(err) {
    console.log("Error occurred while executing search:", err.message);
    response.setStatusCode(500);
    response.setBody(err.message);
  }

};