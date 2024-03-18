
echo 
echo "===================================="
echo "|> Installing App Services assets <|"
echo "===================================="
echo

if ! command -v npm &> /dev/null; then
    echo "npm not found, please install it using NodeJs"
    exit 1
fi

npm install -g atlas-app-services-cli

source .env
echo "Using args:\n"
echo "\tProject API key: ${ATLAS_API_KEY}\n"
echo "\tProject API secret: ${ATLAS_API_PRIVATE_KEY}\n"
echo "\tCluster Name: ${CLUSTER_NAME}\n"
echo "\tApp Name: ${APP_NAME}\n"
echo "\tApp Cloud Provider: ${APP_PROVIDER}\n"
echo "\tApp Region: ${APP_REGION}\n"
echo "\tAzure OpenAI Endpoint: ${AZURE_OPENAI_ENDPOINT}\n"
echo 

appservices login --api-key="${ATLAS_API_KEY}" --private-api-key="${ATLAS_API_PRIVATE_KEY}"

echo "Creating App Services app."

response=$(appservices app create --name "${APP_NAME}" --deployment-model "LOCAL" --provider-region "${APP_PROVIDER}-${APP_REGION}" --cluster "${CLUSTER_NAME}" --cluster-service-name "mongodb-atlas")
echo $response

if ! command -v jq &> /dev/null; then
    echo ">> WARNING <<"
    echo "jq not found."
    echo "Either you need to install it and re-run this script, or  manually set 'APP_SERVICES_ENDPOINT' in .env."
    echo "You will also need to set your Azure OpenAI endpoint in '${APP_NAME}/values/azure-openai-endpoint.json' file before pushing to App Services."
    echo ">> WARNING <<"
    else
    json_response=$(echo $response | grep -o '{.*}')
    client_app_id=$(echo $json_response | jq -r '.client_app_id')

    echo "Found client_app_id: $client_app_id"

    echo 'Writing App Services endppoint to .env for use in other services.'
    if [ -z "$APP_SERVICES_ENDPOINT" ]; then
        echo "\nAPP_SERVICES_ENDPOINT=\"https://$APP_REGION.$APP_PROVIDER.data.mongodb-api.com/app/$client_app_id/endpoint\"" >> .env
        else
        echo "App Services endpoint already exists in .env: $APP_SERVICES_ENDPOINT"
    fi
    echo "Creating Azure Endpoint value from: ${AZURE_OPENAI_ENDPOINT}"
    jq '.value = "'$AZURE_OPENAI_ENDPOINT'"' ./app-services/values/azure-openai-endpoint.json > temp.json && mv temp.json ./app-services/values/azure-openai-endpoint.json
fi

echo "Creating OpenAI secret from key: ${OPENAI_API_KEY}"
appservices secrets create --app "${APP_NAME}" --name "azure-openai-key-secret" --value "${OPENAI_API_KEY}"

echo "App created. Copying files from 'app-services' and pushing ${APP_NAME} to App Services."
cp -r app-services/* ${APP_NAME}
cd ${APP_NAME}
appservices push --yes

echo 
echo "==================================="
echo "|> App Services install finished <|"
echo "==================================="
echo