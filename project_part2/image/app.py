from flask import Flask, render_template, make_response, url_for, jsonify
from flask_cors import CORS
import requests 
import datetime

app = Flask(__name__, static_folder="static")
CORS(app)


# implementation of default GET request with 200 ok response
@app.route('/', methods=['GET'])
def default():
    result = {"message": "Page not found"}
    return make_response(jsonify(result), 200)

@app.route('/image/v1/', methods=['GET'])
def hello():
    result = {"message": "Page not found"}
    return make_response(jsonify(result), 200)

# Route /image/v1/watch/<sku> to get the image regarding to the sku code
@app.route('/image/v1/watch/<sku>', methods=['GET'])
def get_image(sku):
    url = "https://s3-eu-west-1.amazonaws.com/cloudcomputing-2018/project1/images/{}.png".format(sku)
    response = None
    head_response = requests.head(url)
    res = requests.get(url)
    # If the image doesnt exist render a default html instead HTTP 404 
    if(res.status_code != 200 and res.status_code != 304):
        response = make_response(render_template("notfound.html"), res.status_code )
    else:
        # Cache parameters settings: 
            # Cache-Control = max-age = 3600 seconds
            # Expires = 1 hour
            # ETag = Etag of the image retrieved
        expiry_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)  
        response = make_response(render_template("index.html", value=sku), res.status_code)
        response.headers["Expires"] = expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        response.headers['Cache-Control'] = 'max-age=3600'
        response.add_etag(head_response.headers["ETag"])

    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1080, debug=True)