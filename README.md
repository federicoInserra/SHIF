# SHIF
The goal of this project is to build a financial decision support system that leverages an LLM to invoke relevant functions and pull appropriate data from subsystems to help with portfolio management and response to liquidity events in the news.

# Details

- **Project** : SHIF (Something happened In finance)
- **Team Number** : 2
- **Team Name** : Shif Surfers
- **Demonstration Video** : TO BE ADDED

Team members:
- John Underwood
- Paolo Picello
- Federico Inserra
- Loic Kameni
- Aicha Sarr

# Justification

In the ever-evolving landscape of financial portfolio management,investors grapple with the challenge of navigating complex market dynamics and responding effectively to liquidity events highlighted in the news. Existing systems often lack the capability to harness the power of a robust decision support system presents.

Therefore, there is a pressing need for a comprehensive financial solution that seamlessly integrates advanced natural language processing capabilities. Such a system would empower investors to make informed decisions by efficiently invoking and extracting pertinent data from interconnected subsystems leveraging MongoDB Developer Data Platfor all in one solution.

By addressing this need, the proposed solution aims to enhance portfolio management strategies and enable proactive responses to liquidity events, ultimately fostering greater financial resilience and success in the investment landscape.


# Detailed Application Overview

![Image of technical architecture](https://github.com/kamloiic/shif/blob/main/images/architecture.png)

How it works ?

1. User (fund manager) enter the application
2. He see a dashboard with the different customers he is managing
3. Click on a particular customer
4. Customer dashboard: Stocks, Funds, Age, name etc.
5. In a textbox at the top enter the query "_This customer wants to invest more on renewable energy companies. What are some relevant news about that of the last few days?_"
- textSearch endpoint against RSS
- vectorSearch endpoint against RSS
- Send both the results to gpt4 endpoint (RAG) -> show results in the UI
6. Show RSS news
7. Then user ask: "_What could be good fund to invest on for this customer"_? (memory? Otherwise just mention again the topic)
- textSearch endpoint against funds
- vectorSearch endpoint against funds
- Send both the results to gpt4 endpoint (RAG) -> show results in the UI
8. Show pdf or links
9. Then user ask: “What could be good fund to invest on for this customer”?
- textSearch endpoint against funds_brochure
- vectorSearch endpoint against funds_brochure
- Send both the results to gpt4 endpoint (RAG) -> show results in the UI


# Demonstration Script

## Configure Atlas Cluster

* Log-on to your [Atlas account](http://cloud.mongodb.com/) and navigate to your project

* Create an M10 based 3 node replica-set of your choice, running MongoDB version 7.0.

* In the project's Security tab, choose to add a new user.

* Once the cluster has been fully provisioned, you can load the dump data available in the dump folder.

```bash
mongodump --uri="YOUR-URI" --authenticationDatabase=admin --db=shif
```


## Setup the App Services Application

__1. Generate an API Key on Atlas__

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

* Copy all configuration files from your /SHIP folder, to the new App's configuration directory.

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


## Setup the Front-End

This project was created using the React Leafy Library with TS.

Below are the steps to run the project locally

```bash
npm install --force
```

Install all the dependencies, without --force is probably not gonna work depending on your node and react version. Using force option you just disable the warnings

```bash
npm start
```

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.



## Demo Execution

Please refer to the demonstration video here (link TO BE ADDED).
