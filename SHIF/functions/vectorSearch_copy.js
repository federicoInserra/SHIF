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
  
  if(request.body && request.body.filter && request.body.filter != ''){
    search.$search.filter=request.body.filter;
  }
  
  var pipeline = [search];
  
  var project = {
    $project:{}
  }
  
  if(fields && fields != ''){
    fields.split(',').forEach((field)=>{
      project.$project[[field]]=1
    });
    
    pipeline.push(project);
  }
  
      
  try {
    const results = await collection.aggregate(pipeline).toArray();
    response.setStatusCode(200);
    response.setBody(JSON.stringify({results}));

  } catch(err) {
    console.log("Error occurred while executing search:", err.message);
    response.setStatusCode(500);
    response.setBody(err.message);
  }

};