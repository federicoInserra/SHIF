exports = async function(changeEvent) {
    // Get the full document from the change event.
    const doc = changeEvent.fullDocument;

    // Define the OpenAI API url and key.
    const url = "https://shif-surfers-hack.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15"
    // Use the name you gave the value of your API key in the "Values" utility inside of App Services
    const openai_key = context.values.get("azure-openai-key");
    try {
        console.log(`Processing document with id: ${doc._id}`);

        // Call OpenAI API to get the embeddings.
        let response = await context.http.post({
            url: url,
             headers: {
                'api-key': [openai_key],
                'Content-Type': ['application/json']
            },
            body: JSON.stringify({
              // 'content' field from source document
                input: doc.content,
            })
        });

        // Parse the JSON response
        let responseData = EJSON.parse(response.body.text());

        // Check the response status.
        if(response.statusCode === 200) {
            console.log("Successfully received embedding.");

            const embedding = responseData.data[0].embedding;

            // Use the name of your MongoDB Atlas Cluster
            const collection = context.services.get("mongodb-atlas").db("shif").collection("docs_chunks");

            // Update the document in MongoDB.
            const result = await collection.updateOne(
                { _id: doc._id },
                // The name of the new field you'd like to contain your embeddings.
                { $set: { embedding: embedding }}
            );
            
 
        } else {
            console.log(`Failed to receive embedding. Status code: ${response.statusCode}`);
            console.log(JSON.stringify(response))
        }

    } catch(err) {
        console.error(err);
    }
};