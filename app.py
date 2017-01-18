from flask import Flask, request, render_template
from flask.ext.api import status
from flask_cors import CORS
from flask.ext.sqlalchemy import SQLAlchemy
import os, sys, logging

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()
CORS(app)


class Json(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80), unique=False, nullable=True, default=None)
    data = db.Column(db.String(), unique=False)

    def __init__(self, id, password, data):
        self.id = id
        if password:
            self.password = password
        self.data = data

    def __repr__(self):
        return self.data


@app.route("/", methods=["GET"])
def web():
    jsons = None
    try:
        jsons = db.session.query(Json).all()
    except Exception as e:
        print(e)
    return render_template('index.html', jsons=jsons)


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
        if not json_id:
            return ("error you need to provide json id", status.HTTP_404_NOT_FOUND)

        try:
            result = db.session.query(Json).get(json_id)
            if result:
                return str(result)
            else:
                return ("json not found", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return ("error something bad happend", status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # get json
        json_data = request.get_json(force=True)
        # try to get json id
        try:
            json_to_edit_id = json_data['jsonId']
            del json_data['jsonId']
        except:
            # if id is not sent return error
            return ("error you did not send json id", status.HTTP_404_NOT_FOUND)

        try:
            # get json from db
            json_to_edit = db.session.query(Json).get(json_to_edit_id)

        except:
            return ("error json not found", status.HTTP_404_NOT_FOUND)

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
        if json_to_edit.password:
            if str(json_to_edit.password) == str(json_to_edit_password):
                # if json password ok
                json_updated = True
                try:
                    json_to_edit.data = str(json_data)
                    db.session.commit()
                except Exception as e:
                    print(e)

            else:
                # if json password is invalid
                return ("error invalid json password", status.HTTP_404_NOT_FOUND)

            if json_to_edit and json_updated:
                return ("json updated", status.HTTP_200_OK)
            else:
                # did not found json by id
                return ("error not updated", status.HTTP_404_NOT_FOUND)
                # handle edit if not protected
        elif not json_to_edit.password and json_protected:
            return ("why password", status.HTTP_404_NOT_FOUND)
        else:
            json_updated = False
            try:
                json_to_edit.data = str(json_data)
                db.session.commit()
                json_updated = True
            except Exception as e:
                print(e)

            if json_to_edit and json_updated:
                return ("json updated", status.HTTP_200_OK)
            else:
                # did not found json by id
                return ("error json not found", status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        recived_data = request.get_json(force=True)
        try:
            json_to_create_id = recived_data['jsonId']
        except:
            return ("error you need to provide json id", status.HTTP_404_NOT_FOUND)

        try:
            json_has_password = recived_data['jsonPassword']
            del recived_data['jsonPassword']
        except:
            json_has_password = None

        taken = db.session.query(Json).get(json_to_create_id)
        if not taken:
            try:
                del recived_data['jsonId']
                newJsonDB = Json(json_to_create_id, json_has_password, str(recived_data))
                db.session.add(newJsonDB)
                db.session.commit()
            except Exception as e:
                print(e)

        else:
            return ("that id is taken", status.HTTP_403_FORBIDDEN)

        if json_has_password:
            return (
                "json created your json id: " + json_to_create_id + " and pass: " + json_has_password + " remember your password it wont be shown anywhere",
                status.HTTP_201_CREATED)
        else:
            return ("json created your json id: " + json_to_create_id,
                    status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        # try to get json id
        json_id = request.args.get('jsonId')
        if not json_id:
            return ("error you did not send json id", status.HTTP_404_NOT_FOUND)

        json_to_delete = db.session.query(Json).get(json_id)

        if not json_to_delete:
            return ("json not found", status.HTTP_404_NOT_FOUND)
        else:

            if json_to_delete.password:
                json_pass = request.args.get('jsonPassword')
                if not json_pass:
                    return ("json is protected provide password", status.HTTP_400_BAD_REQUEST)
                else:
                    if str(json_to_delete.password) == str(json_pass):
                        db.session.delete(json_to_delete)
                        db.session.commit()
                        return ('json deleted', status.HTTP_200_OK)
                    else:
                        return ('invalid password', status.HTTP_400_BAD_REQUEST)
            else:
                db.session.delete(json_to_delete)
                db.session.commit()
                return ('json deleted', status.HTTP_200_OK)


@app.route('/about', methods=["GET"])
def about():
    return app.send_static_file('about.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
