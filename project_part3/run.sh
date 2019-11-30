pip install --no-cache-dir -r requirements.txt

export FLASK_APP=server.py
export FLASK_ENV=development
export FLASK_RUN_PORT=1080
export HTTP_USER=cloud
export HTTP_PASS=computing

flask run
