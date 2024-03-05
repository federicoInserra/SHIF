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
  var fields = request.query.fields;
  var limit = parseInt(request.query.limit);

  // Get a collection from the context
  var collection = context.services.get(serviceName).db(dbName).collection(collName);
  
  var searchOp = {
    text: {
      query:query,
      path:{wildcard:"*"}
    }
  }
  
  var pipeline = [
    {
      $search: Object.assign({index: searchIndex},searchOp)
    }
  ]
  
  var project = {
    $project:{}
  }
  
  if(fields && fields != ''){
    fields.split(',').forEach((field)=>{
      project.$project[[field]]=1
    });
    
    pipeline.push(project);
  }
  
  if(limit){
    pipeline.push({$limit:limit});
  }
  
  var facetPipeline = [
    {
      $searchMeta:{
        index: searchIndex,
        facet: {
          operator: searchOp,
          facets: {
            stock_symbols: {
              type: "string",
              path: "nasdaq_tickers",
              numBuckets: 25
            },
            links: {
              type: "string",
              path: "parent_link",
              numBuckets: 25
            },
          }
        }
      }
    },
    {
      $project:{
        stock_symbols: {
          $map: {
            input: "$facet.stock_symbols.buckets",
            as: "bucket",
            in: "$$bucket._id"
          }
        },
        links: {
          $map: {
            input: "$facet.links.buckets",
            as: "bucket",
            in: "$$bucket._id"
          }
        }
      }
    }
  ]
  
      
  try {
    const results = await collection.aggregate(pipeline).toArray();
    const facets = await collection.aggregate(facetPipeline).toArray();
    response.setStatusCode(200);
    response.setBody(JSON.stringify({results:results,metadata:facets[0]}));

  } catch(err) {
    console.log("Error occurred while executing search:", err.message);
    response.setStatusCode(500);
    response.setBody(JSON.stringify({err}));
  }

};