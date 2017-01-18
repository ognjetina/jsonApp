from flask import Flask, request, jsonify, render_template, redirect
from flask.ext.api import status
from jsonObject import JsonObject
from flask_cors import CORS
from flask.ext.sqlalchemy import SQLAlchemy
import os
import logging
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
CORS(app)
data = []


class Json(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80), unique=True)
    data = db.Column(db.String(), unique=True)

    def __init__(self, id, password, data):
        self.id = id
        self.password = password
        self.data = data

    def __repr__(self):
        return '<User %r>' % self.data


@app.route("/")
def web():
    jsons = []
    try:
        jsons = Json.query.all()
    except:
        pass
    return render_template('index.html', data=data, jsonsFromDB=jsons)


@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('page_not_found.html')


@app.errorhandler(405)
def page_not_found(e):
    return app.send_static_file('page_not_found.html')


@app.route('/json', methods=["GET", "PUT", "POST", "DELETE"])
def json():
    if request.method == 'GET':
        json_id = request.args.get('jsonId')
        json_found_not_found = True
        if json_id:
            result = ''
            for d in data:
                if str(d.id) == str(json_id):
                    result = d.data
                    json_found_not_found = False
                    break

            if json_found_not_found:
                return ("json not found", status.HTTP_404_NOT_FOUND)

            return jsonify(result)
        else:
            return redirect("/")

    if request.method == 'PUT':
        # get json
        json_data = request.get_json(force=True)
        # try to get json id
        try:
            json_to_edit_id = json_data['jsonId']
            del json_data['jsonId']
        except:
            # if id is not sent return error
            return ("Error you did not send json id", status.HTTP_404_NOT_FOUND)

        try:
            # get json password and remove it from json. set protected flag to True
            json_to_edit_password = json_data['jsonPassword']
            del json_data['jsonPassword']
            if json_to_edit_password:
                json_protected = True
        except:
            # if no json password found set protected flag to False
            json_protected = False

        # handle edit if protected
        if json_protected:
            json_updated = False
            json_found = False
            for d in data:
                # search for json by id
                if str(d.id) == str(json_to_edit_id):
                    # found json by id
                    json_found = True
                    if str(d.password) == str(json_to_edit_password):
                        # if json password ok
                        json_updated = True
                        d.data = json_data
                        break
                    else:
                        # if json password is invalid
                        return ("Error invalid json password", status.HTTP_404_NOT_FOUND)

            if json_found and json_updated:
                return ("json updated", status.HTTP_200_OK)
            else:
                # did not found json by id
                return ("Error json not found", status.HTTP_404_NOT_FOUND)
        # handle edit if not protected
        else:
            json_updated = False
            json_found = False
            for d in data:
                # search for json by id
                if str(d.id) == str(json_to_edit_id):
                    if d.password:
                        return ("Error json is protected!", status.HTTP_404_NOT_FOUND)
                    # found json by id
                    json_found = True
                    json_updated = True
                    d.data = json_data
                    break
            if json_found and json_updated:
                return ("json updated", status.HTTP_200_OK)
            else:
                # did not found json by id
                return ("Error json not found", status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':

        recived_data = request.get_json(force=True)
        newJson = JsonObject(0, "null", None)
        try:
            json_to_create_id = recived_data['jsonId']
        except:
            return ("Error you need to provide json id", status.HTTP_404_NOT_FOUND)
        try:
            json_has_password = recived_data['jsonPassword']
            newJson.password = json_has_password
            del recived_data['jsonPassword']
        except:
            json_has_password = "not set"

        if json_to_create_id:
            # create with custom id if id is not taken
            id_taken = False
            for d in data:
                if str(d.id) == str(json_to_create_id):
                    id_taken = True

            if not id_taken:
                newJson.id = json_to_create_id
            else:
                return ("that id is taken", status.HTTP_403_FORBIDDEN)

        else:
            return ("pls provide json id", status.HTTP_204_NO_CONTENT)

        del recived_data['jsonId']

        try:
            newJson.data = recived_data
            newJsonDB = Json(newJson.id, newJson.password, newJson.data)
            db.session.add(newJsonDB)
            db.session.commit()
            print("save new json to db")
        except:
            print("failed to save json to db")
            pass
        data.append(newJson)

        return (
            "Json created your json id: " + json_to_create_id + " and pass: " + json_has_password + ". Remember your password it wont be shown anywhere!",
            status.HTTP_201_CREATED)

    if request.method == 'DELETE':

        # try to get json id
        json_id = request.args.get('jsonId')

        if json_id:
            # find json and check if exists and is it protected!
            json_found = False

            for d in data:
                if str(d.id) == str(json_id):
                    json_found = True
                    json = d
                    break

            if json_found:
                # go on
                if json.password:
                    json_password = request.args.get('jsonPassword')

                    # if we got password
                    if json_password:
                        if json_password == json.password:
                            data.remove(json)
                            return ("json removed", status.HTTP_200_OK)
                        else:
                            return ("Error invalid json password", status.HTTP_404_NOT_FOUND)
                    # if user forgot password
                    else:
                        return ("Error json is protected and you did not provide password", status.HTTP_404_NOT_FOUND)

                else:
                    data.remove(json)
                    return ("json removed", status.HTTP_200_OK)
            else:
                return ("Error json not found", status.HTTP_404_NOT_FOUND)


        else:
            return ("Error you did not send json id", status.HTTP_404_NOT_FOUND)


@app.route('/about', methods=["GET"])
def about():
    return app.send_static_file('about.html')


if __name__ == "__main__":
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.DEBUG)
    try:
        sys.stdout.write("Starting the app")
        sys.stdout.write("Creating db")
        db.create_all()
    except:
        pass
    app.run(host='0.0.0.0', threaded=True)
