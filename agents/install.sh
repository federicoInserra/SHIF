
echo 
echo "==========================="
echo "|> Installing Agents <|"
echo "==========================="
echo

if ! command -v python3 &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "python3 and pip3 not found, please install them"
    exit 1
    else
    echo "Creating a virtual environment and installing requirements.txt"
    python3 -m venv venv && . venv/bin/activate && pip3 install -r requirements.txt
fi

echo "Install finished. Running the agent API at localhost:3010 with flask and gunicorn"
. venv/bin/activate && gunicorn app:app -b 0.0.0.0:3010 --timeout 120

echo 
echo "============================="
echo "|> Agents install finished <|"
echo "============================="
echo