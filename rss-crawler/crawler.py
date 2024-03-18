import feedparser
from datetime import datetime
import pymongo
from pymongo import ReturnDocument
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import signal
import sys
import traceback
import httpx
from os import getenv
from dotenv import load_dotenv
from time import sleep

load_dotenv('../.env')

class Crawler:
    def __init__(self,FEED_CONFIG,PID):
        self.FEED_CONFIG=FEED_CONFIG
        self.PID=PID
        self.FEED_ID=FEED_CONFIG['_id']
        self.CONN=MongoDBConnection()
        self.MDB_DB=self.CONN.connect()
        self.DRIVER = MyChromeDriver()
        signal.signal(signal.SIGTERM, self.signal_handler)

    def exit(self,status):
        print('Crawler for {} stopping with status {}'.format(self.FEED_ID,status))
        crawl = self.MDB_DB.feeds.find_one_and_update(
            {'_id':self.FEED_CONFIG['_id']},
            {"$set":{'crawl.end':datetime.now(),'status':status}},
            return_document=ReturnDocument.AFTER
        )['crawl']
        crawl.update({'feed_id':self.FEED_CONFIG['_id']})
        self.MDB_DB.logs.insert_one(crawl)
        self.CONN.close()
        self.DRIVER.quit()
        sys.exit(0)

    def signal_handler(self,sig,frame):
        print('SIGTERM received, shutting down')
        self.exit('stopped')
        

    def updateFeed(self,update):
        try:
            self.MDB_DB.feeds.update_one({'_id':self.FEED_CONFIG['_id']},update)
            return
        except Exception as e:
            raise e
    
    def insertEntry(self,session,entry):
        entry.update({'feed_id':self.FEED_ID})
        try:
            docs_collection = self.MDB_DB.docs
            feeds_collection = self.MDB_DB.feeds
            chunks_collection = self.MDB_DB.docs_chunks
            docs_collection.insert_one(entry,session=session)
            chunks = []
            if 'summary' in entry:
                chunks.append(
                    {
                        'parent_id':entry['id'],
                        'parent_link':entry['link'],
                        'type':'summary',
                        'content':"# {title}\n## Summary\n{summary}".format(title=entry['title'][entry['lang']],summary=entry['summary'][entry['lang']])
                    }
                )
            if len(entry['content'][entry['lang']]) > 0:
                for i,paragraph in enumerate(entry['content'][entry['lang']]):
                    chunks.append(
                        {
                            'parent_id':entry['id'],
                            'parent_link':entry['link'],
                            'type':'paragraph',
                            'content':"# {title}\n## Paragraph {number}\n{paragraph}".format(title=entry['title'][entry['lang']],number=i+1,paragraph=paragraph)
                        }
                    )
            for i,chunk in enumerate(chunks):
                chunk.update({'chunk':i})
                if 'tags' in entry:
                    chunk.update({'tags':entry['tags']})
                if 'published' in entry:
                    chunk.update({'published':entry['published']})
                if 'custom_fields' in self.FEED_CONFIG:
                    for field in self.FEED_CONFIG['custom_fields']:
                        if field in entry:
                            chunk.update({field:entry[field]})
            
            chunks_collection.insert_many(chunks,session=session)
            feeds_collection.update_one({'_id':self.FEED_ID},{"$push":{"crawl.inserted":entry['id']}},session=session)
            print("Crawler {}: Entry update transaction successful".format(self.FEED_ID))
            return
        except pymongo.errors.DuplicateKeyError:
            print("Crawl {} entry {} already exists in database".format(self.FEED_ID,entry['id']))
            raise DuplicateEntryException("Entry id {} already exists".format(entry['id']))
        except Exception as e:
            raise e
        
    def processItem(self,item):
        try:
            entry = Entry(
                DATA=item,
                SELECTORS=self.FEED_CONFIG['content_html_selectors'],
                LANG=self.FEED_CONFIG['lang'],
                ATTRIBUTION=self.FEED_CONFIG['attribution'],
                DRIVER=self.DRIVER,
                DATE_FORMAT=self.FEED_CONFIG['date_format'],
                CUSTOM_FIELDS=self.FEED_CONFIG.get('custom_fields',None)
                ).processEntry()
            try:
                with self.CONN.get_session() as session:
                    session.with_transaction(lambda session: self.insertEntry(session,entry))
            except Exception as e:
                print("Crawler {} failed to insert entry for item {}".format(self.FEED_ID,entry['id']),e)
                self.updateFeed({'$push':{'crawl.errors':{'entryId':entry['id'],'error':str(e)}}})
        except Exception as e:
            print("Crawler {} failed to create Entry object for item {}".format(self.FEED_ID,item['id']),e)
            self.updateFeed({'$push':{'crawl.errors':{'entryId':item['id'],'error':str(e)}}})
    
    def start(self):
        config = self.FEED_CONFIG
        crawl = {'pid':self.PID,'start':datetime.now(),'crawled':[],'inserted':[],'errors':[],'duplicates':[]}
        self.updateFeed({"$set":{'crawl':crawl,'status':'running'}})
        try:
            feed = MyFeedParser(config['url']).parseFeed()
        except Exception as e:
            self.updateFeed({'$push':{'crawl.errors':{'error':str(e)}}})
            self.exit('failed')

        for item in feed.entries:
            self.updateFeed({"$push":{"crawl.crawled":item['id']}})
            if self.MDB_DB.docs.find_one({'_id':item['id']},{'_id':1}):
                self.updateFeed({'$push':{'crawl.duplicates':item['id']}})
            else:
                self.processItem(item)
                # backoff so we don't get banned by websites
                sleep(1)

        self.exit('finished')
        return
    
class Entry:
    def __init__(self,DATA,SELECTORS,LANG,ATTRIBUTION,DRIVER,DATE_FORMAT,CUSTOM_FIELDS):
        self.DATA=DATA
        self.SELECTORS=SELECTORS
        self.LANG=LANG
        self.ATTRIBUTION=ATTRIBUTION
        self.DRIVER=DRIVER
        self.DATE_FORMAT=DATE_FORMAT
        self.CUSTOM_FIELDS=CUSTOM_FIELDS
    
    def get(self):
        return self.DATA

    def parseContent(self,html):
        errors = []
        content = []
        try:
            soup = BeautifulSoup(html, "html.parser")
            if len(soup.body) < 1:
                errors.append({'error':"Page returned empty body tag"})   
            
            else:
                tags = []
                for selector in self.SELECTORS:
                    tags += soup.select(selector)
                
                if len(tags) < 1:
                    errors.append("Failed to find content with any selector: {}".format(self.SELECTORS))
                else:
                    for i,tag in enumerate(tags):
                        content.append(tag.text.strip())

            return content,errors
        except Exception as e:
            raise Exception("Failed to parse content. {}".format(traceback.format_exc()))
        
    def processEntry(self):
        entry = self.DATA
        lang = self.LANG
        attribution = self.ATTRIBUTION
        driver = self.DRIVER
        content = {lang:''}
        custom_fields = self.CUSTOM_FIELDS
        try:
            text = ''
            errors = []
            try:
                html = driver.fetchPage(entry.link)
                try:
                    text,errors = self.parseContent(html)
                except Exception as e:
                    raise e
            except EntryParseException as e:
                errors.append({'error':str(e)})
            except Exception as e:
                raise Exception("Failed to fetch page for entry {}. {}".format(entry.link,traceback.format_exc()))
            
            if len(errors) > 0:
                content.update({'errors':errors})
            content.update({lang:text})
            entry.update({'content':content})
            entry.update({'_id':entry.id})
            if 'summary' in entry: entry.update({'summary':{lang:entry.summary}})
            if 'title' in entry: entry.update({'title':{lang:entry.title}})
            if 'published' in entry:
                published_date = ''
                try:
                    published_date = datetime.strptime(entry.published,self.DATE_FORMAT)
                except ValueError as e:
                    print("Failed to parse date {} with format {}. Using current date instead".format(entry.published,self.DATE_FORMAT))
                    published_date = datetime.now()
                entry.update({'published':published_date})
            if 'media_thumbnail' in entry: entry.update({'media_thumbnail':entry.media_thumbnail[0]['url']})
            if 'tags' in entry:
                tagList = []
                for tag in entry.tags:
                    tagList += tag['term'].split(',')
                entry.update({'tags':tagList})
            if 'authors' in entry: entry.update({'authors':[ author['name'] for author in entry.authors if 'name' in author ]})
            if 'author' in entry:
                if not 'authors' in entry:
                    entry.update({'authors':entry.author})
            
            if custom_fields:
                for field in custom_fields:
                    if field in entry:
                        entry.update({field:entry[field].split(',')})
            
            entry.update({'lang':lang})
            entry.update({'attribution':attribution})
            self.DATA = entry
            return self.DATA
        except Exception as e:
            raise e

class MyFeedParser:
    def __init__(self,feed_url):
        self.feed_url = feed_url
    
    def parseFeed(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
            }

            # Create a client that supports HTTP/2
            with httpx.Client(http2=True) as client:
                response = client.get(self.feed_url, headers=headers)
                self.feed = feedparser.parse(response.content)
            return self.feed
        except Exception as e:
            raise Exception("Failed to parse feed url {}. {}".format(self.feed_url,e))

class MongoDBConnection:
    def __init__(self):
        self.url = getenv("MDBCONNSTR")
        self.db_name = getenv("MDB_DB",default="shif")
    
    def connect(self):
        try:
            self.client = pymongo.MongoClient(self.url)
            self.client.admin.command('ping')
            try:
                self.db = self.client.get_database(self.db_name)
                return self.db
            except Exception as e:
                raise Exception("Failed to connect to {}. {}".format(self.db_name,e))
        except Exception as e:
            raise Exception("Failed to connect to MongoDB. {}".format(self.db_name,e))

    def get_session(self):
        return self.client.start_session()

    def close(self):
        self.client.close()

class MyChromeDriver:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = getenv('CHROME_PATH')
        self.options.add_argument("--headless")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')

        # Try to avoid getting blocked
        self.options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6331.0")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        
        self.driver = webdriver.Chrome(service=Service(getenv('CHROMEDRIVER_PATH')),options=self.options)
        self.driver.set_page_load_timeout(5)

    def fetchPage(self,link):
        print("Fetching page from {}".format(link))
        try:
            self.driver.get(link)
            html = self.driver.page_source
            return html
        except TimeoutException as e:
            raise EntryParseException("Failed to fetch page from {}. {}".format(link,e),cause='PageTimeoutError')
        except Exception:
            raise Exception("Fetching page failed. {}".format(traceback.format_exc()))
    
    def quit(self):
        self.driver.quit()
        print("Quitting ChromeDriver")

class DuplicateEntryException(Exception):
    def __init__(self, message):
        super().__init__(message)

class EntryParseException(Exception):
    def __init__(self, message, cause=None):
        super().__init__(message)
        self.cause = cause
    
