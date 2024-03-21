from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import json
from os import getenv
from dotenv import load_dotenv
from pymongo import MongoClient, ReturnDocument
from bson import ObjectId
from os import getenv
from dotenv import load_dotenv
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
from bson.json_util import dumps

load_dotenv()

def returnPrettyJson(data):
    try:
        return jsonify(**json.loads(dumps(data)))
    except TypeError:
        try:
            return jsonify(*json.loads(dumps(data)))
        except TypeError:
            try: 
                return dumps(data)
            except TypeError:
                return repr(data)

def runChat(queryPrompt,systemPrompt):
    return requests.post(f"{getenv('APP_SERVICES_ENDPOINT')}/getGpt35turbo",json={"prompt": queryPrompt,"systemPrompt": systemPrompt}).json()

def runChat4(queryPrompt,systemPrompt):
    return requests.post(f"{getenv('APP_SERVICES_ENDPOINT')}/getGpt4",json={"prompt": queryPrompt,"systemPrompt": systemPrompt}).json()

def formatResults(results):
    return "\n".join([f"{i+1}. From: {result.get('parent_link','')}\n{result['content']}" for i, result in enumerate(results)])

def vectorSearch(query,collName,searchIndex,fields,limit,format=True):
    r = requests.post(f"{getenv('APP_SERVICES_ENDPOINT')}/vectorSearch?query={query}&limit={limit}&numCandidates=100&collName={collName}&searchIndex={searchIndex}&fields={fields}").json()
    results = r['results']
    metadata = r['metadata']
    if format:
        return {
            'results': results,
            'metadata': metadata,
            "formatted": formatResults(results)
        }

    else:
        return {
            'results': results,
            'metadata': metadata,
        }

def textSearch(query,collName,searchIndex,fields,limit,format=True):
    r = requests.get(f"{getenv('APP_SERVICES_ENDPOINT')}/textSearch?query={query}&limit={limit}&collName={collName}&searchIndex={searchIndex}&fields={fields}").json()
    results = r['results']
    metadata = r['metadata']
    if format:
        return {
            'results': results,
            'metadata': metadata,
            "formatted": formatResults(results)
        }

    else:
        return {
            'results': results,
            'metadata': metadata,
        }

def stocksAgent(query,formatted_vector_results,formatted_lexical_results):
    stocksSystemPrompt = """You are a financial analyst providing advice and guidance to a client"""
    stocksQueryPrompt = f"""Review the following information with respect to the client's query: {query}.
    You must provide a list of stock symbols that would be of interest in the form:{{"stocks":[<list of symbols>]}}
    Here are the results of the vector searches:
    {formatted_vector_results}
    Here are the results of the lexical searches:
    {formatted_lexical_results}
    Only provide the stock symbols as a valid json response. Do not provide any other information."""

    return runChat(stocksQueryPrompt,stocksSystemPrompt)

def queryExpansionAgent(query):
    query = "I am interested in investing more on companies active on climate change."
    systemPrompt = """You are a reasoning engine tasked with providing financial guidance.
    You have access to the following data in MongoDB:
    - A collection of nasdaq and business news article chunks with the following fields: title, summary, content, tags, nasdaq_tickers.
    - A collection of fund chunks with the following fields: fund_name, content.
    - A lexical search index on the chunked data which is good for matching keywords and phrases.
    - A vector search index on the embedded chunked data which is good for semantic search.
    """
    queryPrompt = f"""Create three phrases which can be embedded for vector search, and three phrases for lexical search, to retrieve data to use in a gpt prompt to answer this query: {query}
    You must provide your answer in the form {{"vector":[<vector search phrases>], "lexical":[<lexical search phrases>]}}"""

    return runChat(queryPrompt,systemPrompt)

def resultPickerAgent(query,formattedResults):
    systemPrompt = """You are a financial analyst providing advice and guidance to a client"""
    queryPrompt = f"""Pick the 5 results that can best be used to address the client's query: {query}.
    Explain why you chose them.
    You must provide your answer in the form:{{"results":[{{"title":<result title>,"content":<result content>}}],"explanation":<explanation>}}
    Here are the results:
    {formattedResults}"""
    
    return runChat(queryPrompt,systemPrompt)

def run(query,state_id):
    try:
        print("Calling query expansion agent...")
        searchPhrases = queryExpansionAgent(query)
        queries = json.loads(searchPhrases)

        mdb.update_one({'_id':state_id},{'$set':{'searchPhrases':queries},'$push':{'stages_complete':"Query Expansion"}})

        vectorQuery = " ".join([query for query in queries['vector']])
        lexicalQuery = " ".join([query for query in queries['lexical']])

        print("Running searches...")
        news_vector_results = vectorSearch(vectorQuery,'docs_chunks','vectorIndex','content,parent_link',10)
        news_lexical_results = textSearch(lexicalQuery,'docs_chunks','searchIndex','content,parent_link',10)
        funds_vector_results = vectorSearch(vectorQuery,'funds_chunks','vectorIndex','fund_name,source',10,False)
        mdb.update_one(
            {'_id':state_id},
            {
                '$set':
                    {
                        'search_results':
                            {
                                "news":{"lexical":news_lexical_results,"vector":news_vector_results},
                                "funds":{"vector":funds_vector_results}
                            },
                        'funds':funds_vector_results['metadata']
                    },
                '$push':{'stages_complete':"Run Searches"}
            }
        )

        formatted_vector_results = news_vector_results['formatted']
        formatted_lexical_results = news_lexical_results['formatted']

        print("Running result picking agent...")
        vector_summary = json.loads(resultPickerAgent(query,formatted_vector_results))
        lexical_summary = json.loads(resultPickerAgent(query,formatted_lexical_results))

        mdb.update_one({'_id':state_id},{'$set':{"explanation":{"lexical":lexical_summary,"vector":vector_summary}},'$push':{'stages_complete':"Result Ranking"}})

        print("Running stocks agent...")
        stocksAnswer = stocksAgent(query,formatted_vector_results,formatted_lexical_results)

        stocks = set(json.loads(stocksAnswer)['stocks'])
        links = set()
        stocks.update(news_vector_results['metadata']['stock_symbols']+news_lexical_results['metadata']['stock_symbols'])
        links.update(news_vector_results['metadata']['links']+news_lexical_results['metadata']['links'])

        mdb.update_one(
            {'_id':state_id},
            {
                '$push':{'stages_complete':["Extract Stock Symbols"]},
                '$set':{'stocks':list(stocks),'links':list(links)}
            }
        )

        vector_formatted = "\n".join([f"# {r['title']}\n# Content\n{r['content']}" for r in vector_summary['results']])
        lexical_formatted = "\n".join([f"# {r['title']}\n# Content\n{r['content']}" for r in lexical_summary['results']])
        links_string = "\n".join(list(links)[:10])
        stocks_string = ",".join(stocks)

        finalSystemPrompt = """You are a financial analyst providing advice and guidance to a client."""
        finalUserPrompt = f"""Provide a detailed summary of the information you have gathered for the client's query: {query}.
        You must reference specific companies, funds and stocks and news articles where appropriate.
        Do not reference the lexical or vector search results directly.
        Vector Search results:
        {vector_formatted}
        Explanation:
        {vector_summary['explanation']}
        Lexical Search results:
        {lexical_formatted}
        Explanation:
        {lexical_summary['explanation']}
        relevant links:
        {links_string}"""

        print("Getting final answer")
        answer = runChat(finalUserPrompt,finalSystemPrompt)
        mdb.update_one(
            {'_id':state_id},
            {
                '$set':{'answer':answer,'final_prompt':{'user':finalUserPrompt,'system':finalSystemPrompt},'status':'finished'},
            }
        )
        print("Done!")

    except Exception as e:
        mdb.update_one(
            {'_id':state_id},
            {
                '$set':{'answer':str(e),'final_prompt':{'user':finalUserPrompt,'system':finalSystemPrompt},'status':'error'},
            }
        )

    # return (final)
    # return returnPrettyJson({'answer':answer,'explanation':{'lexical':lexical_summary['explanation'],'vector':vector_summary['explanation']},'stocks':list(stocks),'links':list(links),'funds':funds_vector_results['metadata']})

  
mongo_db_name = getenv("MDB_DB",default="shif")
mongo_coll_name = 'requests'
mongo_client = MongoClient(getenv('MDBCONNSTR'))
mdb = mongo_client[mongo_db_name][mongo_coll_name]

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.get("/advice")
def advice():    
    query = request.args.get('q', default = "", type = str)
    r = mdb.insert_one({'query':query,'timestamp':datetime.now(),'stages_complete':[],"status":"processing"})
    print("query: ",query)
    executor = ThreadPoolExecutor()
    executor.submit(run, query, r.inserted_id)
    executor.shutdown(wait=False)
    print("*****************")

    return returnPrettyJson({"_id":r.inserted_id,query:query,'stages_complete':[],"status":"processing"})
    # return {"_id":r.inserted_id,query:query,'stages_complete':[],"status":"processing"}

@app.get("/status")
def status(): 
    id = request.args.get('id', default = "", type = str)
    r = mdb.find_one({'_id':ObjectId(id)})
    return returnPrettyJson(r)