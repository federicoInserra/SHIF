# SHIF
The goal of this project is to build a financial decision support system that leverages an LLM to invoke relevant functions and pull appropriate data from subsystems to help with portfolio management and response to liquidity events in the news.

# Details

- **Project** : SHIF (Something happened In finance)
- **Team Number** : 2
- **Team Name** : Shif Surfers
- **Demonstration Video** : [Presentation (4m20s)](https://youtu.be/a6uoUfoZuhM) | [Demo (6m34s)](https://youtu.be/JlPs1-LmRMg)

**Team members**:
- John Underwood
- Paolo Picello
- Federico Inserra
- Loic Kameni
- Aicha Sarr

# Justification

In the ever-evolving landscape of financial portfolio management,investors grapple with the challenge of navigating complex market dynamics and responding effectively to liquidity events highlighted in the news. Existing systems often lack the capability to harness the power of a robust decision support system.

Therefore, there is a pressing need for a comprehensive financial solution that seamlessly integrates advanced natural language processing capabilities. Such a system would empower investors to make informed decisions by efficiently invoking and extracting pertinent data from interconnected subsystems leveraging MongoDB Developer Data Platform all in one solution.

By addressing this need, the proposed solution aims to enhance portfolio management strategies and enable proactive responses to liquidity events, ultimately fostering greater financial resilience and success in the investment landscape.


# Detailed Application Overview

![Image of technical architecture](https://github.com/federicoInserra/SHIF/blob/main/images/architecture.png)

How it works ?

1. User (fund manager) enter the application
2. He sees a dropdown menu with the different customers he is managing
3. Click on a particular customer
4. Customer dashboard: Stocks, Funds, Age, name etc.
5. In a textbox at the top enter the query "My customer want to invest more on chinese companies"
6. And endpoint is called on the back-end and this is orchestrating different LLM agents runnning as Python functions (one agent is doing stock suggestions, another is assessing results and explaining why the results are good sources for answering client questions, another takes querys as input and performs query expansion on the actual query, another performs re-rank)
6. The results are then rendered on the UI to show relevant information
7. Different Atlas charts are rendered in the UI as well
8. You can also see the raw JSON outpu from the LLM

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

## Setup the Backend-End

This project was created using Flask as Python server to orchestrate the different LLM agents running on Atlas App Services.
In order to start the server run

```bash
cd agents
./install.sh
```

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

Please refer to the demonstration videos linked above.
