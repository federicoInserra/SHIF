exports = async function getTextEmbeddingAda(query) {
    // Define the OpenAI API url and key.
    //const url =  context.values.get("azure-openai-endpoint");
    const openai_key = context.values.get("azure-openai-key");
    const url = "https://shif-surfers-hack.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15";
    try{
       let response = await context.http.post({
              url: url,
               headers: {
                  'api-key': [openai_key],
                  'Content-Type': ['application/json']
              },
              body: JSON.stringify({
                input: query,
              })
          });
      let responseData = EJSON.parse(response.body.text());
      if(response.statusCode === 200) {
          console.log("Successfully received text embedding.");
          return responseData.data[0].embedding;
      }
      else {
          console.log(`Failed to get embedding. Status code: ${response.status}`);
      }
    } catch(err) {
        console.error(err);
   }
}