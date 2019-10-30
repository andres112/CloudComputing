from flask import Flask, render_template, make_response, url_for
from flask_cors import CORS
import requests 
import datetime
# import pdb

app = Flask(__name__, static_folder="static")
CORS(app)


@app.route('/image/v1/watch/<sku>', methods=['GET'])
def get_image(sku):
    response = requests.get("https://s3-eu-west-1.amazonaws.com/cloudcomputing-2018/project1/images/{}.png".format(sku)) 
    # pdb.set_trace()
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)    
    
    if(response.status_code != 200):
        response = make_response(render_template("notfound.html"), response.status_code )
    else:
        response = make_response(render_template("index.html", value=sku), response.status_code)
        response.headers["Expires"] = expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        response.headers['Cache-Control'] = 'max-age=3600'
        response.add_etag()

    # Return response 
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1080, debug=True)