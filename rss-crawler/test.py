from crawler import MyChromeDriver,MongoDBConnection

try:
    driver = MyChromeDriver()
    html = driver.fetchPage("https://www.google.com")
    page_length = len(html)
    connection=MongoDBConnection()
    db=connection.connect()
    try:
        assert page_length > 0
    except AssertionError as e:
        print(str(e))
        print("Failed")
        exit()
    try:
        assert db is not None
    except AssertionError as e:
        print(str(e))
        print("Failed")
        exit()
except Exception as e:
    print(str(e))
    print("Failed")
    exit()
connection.close()
print("Passed")
exit()

