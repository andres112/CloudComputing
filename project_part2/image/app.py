from flask import Flask, render_template, make_response, url_for, jsonify
from flask_cors import CORS
import requests 
import datetime
import pdb

app = Flask(__name__, static_folder="static")
CORS(app)


@app.route('/', methods=['GET'])
def default():
    result = {"message": "No message"}
    return make_response(jsonify(result), 200)

@app.route('/image/v1/', methods=['GET'])
def hello():
    result = {"message": "No message"}
    return make_response(jsonify(result), 200)

@app.route('/image/v1/watch/<sku>', methods=['GET'])
def get_image(sku):
    url = "https://s3-eu-west-1.amazonaws.com/cloudcomputing-2018/project1/images/{}.png".format(sku)
    response = None
    head_response = requests.head(url)
    res = requests.get(url)
    # pdb.set_trace()
    if(res.status_code != 200 and res.status_code != 304):
        response = make_response(render_template("notfound.html"), res.status_code )
    else:
        expiry_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)  
        response = make_response(render_template("index.html", value=sku), res.status_code)
        response.headers["Expires"] = expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        response.headers['Cache-Control'] = 'max-age=3600'
        response.add_etag(head_response.headers["ETag"])

    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1080, debug=True)