echo "Running the agent API at localhost:3010 with flask and gunicorn"
. venv/bin/activate && gunicorn app:app -b 0.0.0.0:3010
