exports = async function getGpt4(request,response) {
    
    if(request.body){
      // Convert the request body to a JSON string
      const serialized = request.body.text();
      // Parse the string into a usable object
      const body = EJSON.parse(serialized)
      if(body){
        customerId = body.customerId;
      }
    }
 
    
    const collection = context.services.get("mongodb-atlas").db("shif").collection("customers");
    
    const result = await collection.findOne(
        { customerId: customerId }
    );
    
    return result
};
