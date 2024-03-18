import os.path
from os import path
from langchain.document_loaders import PyPDFLoader
from pymongo import MongoClient
import os
import time
from os import getenv
from dotenv import load_dotenv

load_dotenv('../.env')

mongo_db_name = getenv("MDB_DB",default="shif")
mongo_coll_name = 'funds_chunks'

mongo_client = MongoClient(getenv('MDBCONNSTR'))
mongo_coll = mongo_client[mongo_db_name][mongo_coll_name]
mongo_db_and_coll_path = '{}.{}'.format(mongo_db_name, mongo_coll_name)

mongo_coll.delete_many({})

# Delete existing documents -- run before demo

chunked_docs = {}

cwd = os.getcwd()

# Just needed in case you'd like to append it to an array
folder_path = cwd + '/documents'

print(folder_path)

# List documents in the folder
for fund in os.listdir(folder_path):
    fund_path = folder_path + "/" + fund
    if(os.path.isdir(fund_path)):
      print("fund name: " + fund)

      for filename in os.listdir(fund_path):
        if filename.endswith('pdf'):
          loader = PyPDFLoader(os.path.join(fund_path, filename))
          chunked_docs[filename, fund] = loader.load_and_split()
          print('computed ' + str(len(chunked_docs[filename, fund])) + ' chunks for document: ' + filename)
      print('----')

#print(chunked_docs)


for key,value in chunked_docs.items():
  #print("Fund name: " + key[1])
  #print("Document name: " + key[0])
  #print("Number of chunks: " + str(len(value)))

  for i in range(len(value)):
    text = value[i].page_content

    document = {
      "fund_name": key[1],
      "source": key[0],
      "content": text,
      "chunk_id": i
    }
  
    mongo_coll.insert_one(document)
    time.sleep(1) 

