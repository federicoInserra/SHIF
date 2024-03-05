exports = async function getGpt4(request,response) {

    // Define the OpenAI API url and key.
    //const url =  context.values.get("azure-openai-endpoint");
    const openai_key = context.values.get("azure-openai-key");
    const url = "https://shif-surfers-hack.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2023-05-15";
    
    var query = request.query.query;
    var prompt = request.query.prompt
    
    // Convert the request body to a JSON string
    const serialized = request.body.text();
    // Parse the string into a usable object
    const body = EJSON.parse(serialized)
    if(body){
      query = body.prompt;
      prompt = body.systemPrompt
    }
 
    try{
       let response = await context.http.post({
              url: url,
               headers: {
                  'api-key': [openai_key],
                  'Content-Type': ['application/json']
              },
              body: JSON.stringify({
                messages: [
                  {"role": "system", "content": prompt && prompt != "" ? prompt : "You are a helpful assistant."},
                  {"role": "user", "content": query}
                  ]})
          });
      
      console.log("System prompt:",prompt);
      console.log("Query prompt:",query);
      
      let responseData = EJSON.parse(response.body.text());
      
      if(response.statusCode === 200) {
          console.log("Successfully received message.");
          console.log(responseData.choices[0].message.content);
          return responseData.choices[0].message.content;
      } 
      else {
          console.log(`Failed to get result. Status code: ${response.statusCode}`);
      }
    
    } catch(err) {
        console.error(err);
   }
}