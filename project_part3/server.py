from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from functools import wraps
import boto3

import app_controller

app = Flask(__name__)
CORS(app)

# app.config['HTTP_USER'] = os.getenv('HTTP_USER')
# app.config['HTTP_PASS'] = os.getenv('HTTP_PASS')
app.config['HTTP_USER'] = "cloud"
app.config["HTTP_PASS"] = "computing"
TABLE_NAME = 'watches'

dynamo_client = boto3.client('dynamodb')

# HTTP Basic Authentication function

def authentication(f):
    @wraps(f)
    def setAuth(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == app.config['HTTP_USER'] and auth.password == app.config["HTTP_PASS"]:
            return f(*args, **kwargs)

        return make_response("User not verified!", 401, {'WWW-Authenticate': 'Basic realm="Loging Required'})
    return setAuth

# Handle / route
@app.route('/', methods=['GET'])
@authentication
def default():
    result = {"message": "Initial page"}
    return make_response(jsonify(result), 200)


# POST /watch/
@app.route('/info/v2/watch', methods=['POST'])
@authentication
def create_sku():
    try:
        if request.method == 'POST':            
            result = app_controller.put_watch()

            if 'error' in result:
                return make_response(jsonify(result), 400)
            else:
                return make_response(jsonify(result), 200)
    except Exception as e:
        result = {"error": str(e)}
        return make_response(jsonify(result), 400)

# GET /watch/{sku}
@app.route('/info/v2/watch/<sku>', methods=['GET'])
def skuOperations(sku):
    try:
        result = app_controller.get_watch(sku)

        if( result):
            response = make_response(jsonify(result), 200)
            response.headers['Cache-Control'] = 'max-age=3600'
            print(response)
            return response
        else:
            result = {"error": "There are not registers for {}".format(sku)}
            return make_response(jsonify(result), 404)
    except Exception as e:
        result = {"error": str(e)}
        return make_response(jsonify(result), 400)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1080, debug=True)