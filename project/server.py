from flask import Flask, jsonify, request, make_response
from functools import wraps
from flask_cors import CORS
import pymysql.cursors
import time
import os

app = Flask(__name__)
CORS(app)

# Set up the ENV variables
app.config['HOST'] = os.getenv('DB_HOST')
app.config['PORT'] = os.getenv('DB_PORT')
app.config['DBNAME'] = os.getenv('DB_DBNAME')
app.config['USER'] = os.getenv('DB_USER')
app.config['PASS'] = os.getenv('DB_PASS')

app.config['HTTP_USER'] = os.getenv('HTTP_USER')
app.config['HTTP_PASS'] = os.getenv('HTTP_PASS')

# app.config['HOST'] = "localhost"
# app.config['DBNAME'] = "watches"
# app.config['USER'] = "watches"
# app.config['PASS'] = "watches"
# app.config['HTTP_USER'] = "cloud"
# app.config['HTTP_PASS'] = "computing"


# Connection to MySQL data base
def dbConnection():
    return pymysql.connect(host=app.config['HOST'],
                           user=app.config['USER'],
                           password=app.config['PASS'],
                           db=app.config['DBNAME'],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

# HTTP Basic Authentication function


def authentication(f):
    @wraps(f)
    def setAuth(*args, **kwargs):
        if request.authorization and request.authorization.username == app.config["HTTP_USER"] and request.authorization.password == app.config["HTTP_PASS"]:
            return f(*args, **kwargs)
        else:
            return make_response("User not verified!", 401, {'WWW-Authenticate': 'Basic realm="Loging Required'})
    return setAuth

# Get values of the enum and set datatypes for validations


def getValuesFromDB():
    connection = dbConnection()
    try:
        with connection.cursor() as cursor:
            # Read a single record
            setValuesQuery = ("select col.column_name as name, trim(leading 'set' from col.column_type) as data "
                              "from information_schema.columns col "
                              "where col.data_type in ('set') "
                              "and col.table_schema=%s")
            enumValuesQuery = ("select col.column_name as name, trim(leading 'enum' from col.column_type) as data "
                               "from information_schema.columns col "
                               "where col.data_type in ('enum') "
                               "and col.table_schema=%s")
            cursor.execute(setValuesQuery, (app.config['DBNAME'],))
            setResult = cursor.fetchall()
            cursor.execute(enumValuesQuery, (app.config['DBNAME'],))
            enumResult = cursor.fetchall()

            result = setResult + enumResult
    finally:
        connection.close()

# Validate if the attribute in body is undefined, null or empty


def validateData(dataname):
    return dataname in request.json and len(str(request.json[dataname])) > 0 and request.json[dataname] != None

# HTTP Routes handlers
# POST: /watch
@app.route('/info/v1/watch', methods=['POST'])
@authentication
def create():
    connection = dbConnection()
    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                watch = {
                    'sku': request.json["sku"] if validateData("sku") else None,
                    'type': request.json["type"] if validateData("type") else "watch",
                    'status': request.json["status"] if validateData("status") else "current",
                    'gender': request.json["gender"] if validateData("gender") else "None",
                    'year': request.json["year"] if validateData("year") else "0",
                    'dial_material': request.json["dial_material"] if validateData("dial_material") else "",
                    'dial_color': request.json["dial_color"] if validateData("dial_color") else "",
                    'case_material': request.json["case_material"] if validateData("case_material") else "",
                    'case_form': request.json["case_form"] if validateData("case_form") else "",
                    'bracelet_material': request.json["bracelet_material"] if validateData("bracelet_material") else "",
                    'movement': request.json["movement"] if validateData("movement") else ""}

                sql = ("INSERT INTO watches"
                       " (sku, type, status, gender, year, dial_material, dial_color,"
                       " case_material, case_form, bracelet_material, movement)"
                       " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

                cursor.execute(sql, (watch["sku"], watch["type"], watch["status"], watch["gender"], watch["year"],
                                     watch["dial_material"], watch["dial_color"], watch["case_material"],
                                     watch["case_form"], watch["bracelet_material"], watch["movement"],))
                connection.commit()
                result = {
                    "message": "Register {} created successfuly".format(watch["sku"])}
    except pymysql.MySQLError as e:
        result = {"error": str(e)}
        return make_response(jsonify(result), 400)
    finally:
        connection.close()
    return make_response(jsonify(result), 200)

# GET, PUT, DELETE: /watch/{sku}
@app.route('/info/v1/watch/<sku>', methods=['GET', 'DELETE', 'PUT'])
@authentication
def skuOperations(sku):
    getValuesFromDB()
    connection = dbConnection()
    try:
        with connection.cursor() as cursor:
            # Get data base on sku id by default
            skuQuestion = "SELECT * FROM `watches` WHERE `sku`=%s"
            cursor.execute(skuQuestion, (sku,))
            result = cursor.fetchone()

            if(result):
                # Update operation rely on the sku id
                if request.method == "PUT":
                    watch = {
                        'type': request.json["type"] if validateData("type") else result["type"],
                        'status': request.json["status"] if validateData("status") else result["status"],
                        'gender': request.json["gender"] if validateData("gender") else result["gender"],
                        'year': request.json["year"] if validateData("year") else result["year"],
                        'dial_material': request.json["dial_material"] if validateData("dial_material") else result["dial_material"],
                        'dial_color': request.json["dial_color"] if validateData("dial_color") else result["dial_color"],
                        'case_material': request.json["case_material"] if validateData("case_material") else result["case_material"],
                        'case_form': request.json["case_form"] if validateData("case_form") else result["case_form"],
                        'bracelet_material': request.json["bracelet_material"] if validateData("bracelet_material") else result["bracelet_material"],
                        'movement': request.json["movement"] if validateData("movement") else result["movement"]}

                    sql = ("UPDATE watches"
                           " SET type=%s, status=%s, gender=%s, year=%s, dial_material=%s,"
                           " dial_color=%s, case_material=%s, case_form=%s, bracelet_material=%s, movement=%s"
                           " WHERE sku=%s")
                    cursor.execute(sql, (watch["type"], watch["status"], watch["gender"], watch["year"],
                                         watch["dial_material"], watch["dial_color"], watch["case_material"],
                                         watch["case_form"], watch["bracelet_material"], watch["movement"], sku,))
                    connection.commit()
                    result = {
                        "message": "Register {} updated successfuly".format(sku)}

                # Delete operation rely on the sku id
                if request.method == "DELETE":
                    sql = "DELETE FROM `watches` WHERE `sku`=%s"
                    cursor.execute(sql, (sku,))
                    connection.commit()
                    result = {
                        "message": "Register {} deleted successfuly".format(sku)}

                return make_response(jsonify(result), 200)

            else:
                result = {
                    "error": "Thera are not registers for {}".format(sku)}
                return make_response(jsonify(result), 404)

    except pymysql.MySQLError as e:
        result = {"error": str(e)}
        return make_response(jsonify(result), 400)
    finally:
        connection.close()


# GET: /watch/complete-sku{prefix}
@app.route('/info/v1/watch/complete-sku/<prefix>', methods=['GET'])
@authentication
def getByPrefix(prefix):
    connection = dbConnection()
    try:
        with connection.cursor() as cursor:
            # Get data based on sku prefix id
            prefixQuestion = "SELECT * FROM `watches` WHERE `sku` LIKE \'{}\' ".format(
                prefix+'%')
            cursor.execute(prefixQuestion)
            result = cursor.fetchall()

            # Response validation
            if result:
                return make_response(jsonify(result), 200)
            else:
                result = {
                    "error": "There are not registers for {} ".format(prefix)}
                return make_response(jsonify(result), 404)

    except pymysql.MySQLError as e:
        result = {"error": str(e)}
        return make_response(jsonify(result), 400)
    finally:
        connection.close()
    

# GET: /watch/find
@app.route('/info/v1/watch/find', methods=['GET'])
@authentication
def getByParameters():
    getValuesFromDB()
    connection = dbConnection()
    request_Params = ""
    try:
        with connection.cursor() as cursor:
            # get data from URL sring params
            sku = request.args.get('sku')
            watch_type = request.args.get('type')
            status = request.args.get('status')
            gender = request.args.get('gender')
            year = request.args.get('year')

            # Validate the string params
            parameters = {"sku": sku, "type": watch_type,
                          "status": status, "gender": gender, "year": year}
            for key, value in parameters.items():
                if value != None:
                    if len(request_Params) > 0:
                        request_Params = request_Params + " AND"
                    if key == "sku":
                        request_Params = request_Params + \
                            ' {} LIKE \'{}\''.format(key, value+'%')
                    else:
                        request_Params = request_Params + \
                            ' {} = \'{}\''.format(key, value)

            # SQL question, It only include the params different of None
            prefixQuestion = "SELECT * FROM `watches` WHERE {}".format(
                request_Params)
            cursor.execute(prefixQuestion)
            result = cursor.fetchall()

            # Response validation
            if result:
                return make_response(jsonify(result), 200)
            else:
                result = {
                    "error": "There are not registers according to the options"}
                return make_response(jsonify(result), 404)

    except pymysql.MySQLError as e:
        result = {"error": str(e)}
        return make_response(jsonify(result), 400)
    finally:
        connection.close()


if __name__ == "__main__":
    app.run(port=1080)
