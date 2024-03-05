exports = async function getGpt4(request,response) {

    // Define the OpenAI API url and key.
    //const url =  context.values.get("azure-openai-endpoint");
    const openai_key = context.values.get("azure-openai-key");
    const url = "https://shif-surfers-hack.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2023-05-15";
    
    var query = request.query.query;
    var prompt = request.query.prompt
    
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
