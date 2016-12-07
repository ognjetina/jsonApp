from flask import Flask, request, jsonify, render_template, redirect
from flask.ext.api import status
from jsonObject import JsonObject

app = Flask(__name__)

data = []
next_id = 0


@app.route("/")
def web():
    return render_template('index.html', data=data)


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
        if json_id:
            result = ''
            for d in data:
                if str(d.id) == str(json_id):
                    result = d.data
            if not result:
                return ("", status.HTTP_404_NOT_FOUND)

            return jsonify(result)
        else:
            return redirect("/")

    if request.method == 'PUT':
        json_data = request.get_json(force=True)
        json_to_edit_id = json_data['jsonId']
        if json_to_edit_id:
            del json_data['jsonId']
            json_found = False
            for d in data:
                if str(d.id) == str(json_to_edit_id):
                    d.data = json_data
                    json_found = True

            if json_found:
                return ("", status.HTTP_200_OK)
            else:
                return ("", status.HTTP_404_NOT_FOUND)
        else:
            return ("", status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        global next_id
        next_id = next_id + 1
        recived_data = JsonObject(next_id, request.get_json(force=True))
        data.append(recived_data)
        return ("", status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        json_id = request.args.get('jsonId')
        if json_id:
            json_found = False
            for d in data:
                if str(d.id) == str(json_id):
                    data.remove(d)
                    json_found = True

            if json_found:
                return ("", status.HTTP_200_OK)
            else:
                return ("", status.HTTP_404_NOT_FOUND)
        else:
            return ("", status.HTTP_404_NOT_FOUND)


@app.route('/about', methods=["GET"])
def about():
    return app.send_static_file('about.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
