
echo 
echo "==========================="
echo "|> Installing RSS Crawler <|"
echo "==========================="
echo
if ! command -v npm &> /dev/null; then
    echo "npm not found, please install it using NodeJs"
    exit 1
fi
if ! command -v npx &> /dev/null \
    && ! npm list -g --depth=0 @puppeteer/browsers &> /dev/null \
    && ! npm list --depth=0 @puppeteer/browsers &> /dev/null;
    then
    npm install
fi
if [ ! -f ../.env ]; then
    echo ".env file does not exist. Please create it using example.env and re-run this script."
    exit 1
fi

source ../.env
if [ -z "$CHROME_PATH" ]; then
    CHROME_PATH=$(npx @puppeteer/browsers install chrome-headless-shell@124.0.6331.0 | tail -n 1 | cut -d ' ' -f 2-)
    echo "\nCHROME_PATH=\"$CHROME_PATH\"" >> ../.env
fi
if [ -z "$CHROMEDRIVER_PATH" ]; then
    CHROMEDRIVER_PATH=$(npx @puppeteer/browsers install chromedriver@124.0.6331.0 | tail -n 1 | cut -d ' ' -f 2-)
    echo "CHROMEDRIVER_PATH=\"$CHROMEDRIVER_PATH\"" >> ../.env
fi

echo "Chrome installed at:\n\t$CHROME_PATH"
echo "ChromeDriver installed at:\n\t$CHROMEDRIVER_PATH"
echo "If these paths don't look right check the 'chrome-headless-shell' and 'chromedriver' folders and uppdate your .env file"

if ! command -v python3 &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "python3 and pip3 not found, please install them"
    exit 1
    else
    echo "Creating a virtual environment and installing requirements.txt"
    python3 -m venv venv && . venv/bin/activate && pip3 install -r requirements.txt
fi

echo "Install finished. Running test.py"
TEST_OUTPUT=$(. venv/bin/activate && python3 test.py)
TEST_RESULT=$(echo $TEST_OUTPUT | tail -n 1 | rev | cut -d ' ' -f 1 | rev)
echo "$TEST_RESULT"
if [ "$TEST_RESULT" != "Passed" ]; then
    echo "Test failed"
    echo "$TEST_OUTPUT"
    exit 1
    else
    echo "Test passed. Adding feed configs in feeds.py to MongoDB"
    . venv/bin/activate && python3 setupCollections.py && python3 installFeeds.py
fi

echo 
echo "================================="
echo "|> RSS Crawler install finished<|"
echo "================================="
echo
echo "> You can now run the crawler using 'python3 runCrawl.py' <"
echo