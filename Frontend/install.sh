
echo 
echo "==========================="
echo "|> Installing Frontend <|"
echo "==========================="
echo

if ! command -v npm &> /dev/null; then
    echo "npm not found, please install it using NodeJs"
    exit 1
fi

npm install
npm run build

echo 
echo "============================="
echo "|> Frontend install finished <|"
echo "============================="
echo