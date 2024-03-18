# Setup the App Services Application

__1. Generate an API Key__

* __Generate__ a new __Programmatic API Key__ (record the public and private keys ready for subsequent use). Create the key with the 'Project Owner' permission as it needs permissions to push the app.

__2. Install App Services CLI__

* Ensure App Services CLI is [installed](https://docs.mongodb.com/realm/deploy/realm-cli-reference/#installation), e.g.:

```bash
npm install -g atlas-app-services-cli
```

__3. Configure App Services Environment__

* Using the same __Programmatic API Key__ you created before, login to Realm:

```bash
appservices login --api-key="ATLAS-API-PUBLIC-KEY" --private-api-key="ATLAS-API-PRIVATE-KEY"
```

* Create a new app:

```bash
appservices app create --name "YOUR-APP-NAME" --deployment-model "LOCAL" --provider-region "YOUR-REGION"
```

This will create a new app configuration directory in your root directory.

* Copy all configuration files from your /SHIF folder, to the new App's configuration directory.

* Now import the application

```bash
cd YOUR-DIRECTORY
appservices push
```

* Set up secrets and values for your Azure OpenAI credentials

Create a new Value :
- name : azure-openai-key-secret
- Type : Secret
- Then paste in your OpenAI API key

Then, create another value:
- name : azure-openai-key
- Type: this time, a Value
- And link it to your secret. This is how you will securely reference our API key
