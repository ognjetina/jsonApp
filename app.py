from flask import Flask, request, jsonify, render_template
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
    return "wrong method mate"


@app.route('/add_json', methods=["PUT", "POST"])
def add_json():
    global next_id
    next_id = next_id + 1
    recived_data = JsonObject(next_id, request.get_json(force=True))
    data.append(recived_data)
    return "your json has id: " + str(next_id)


@app.route('/get_json', methods=["GET"])
def get_json():
    json_id = request.args.get('jsonId')
    result = ''
    for d in data:
        if str(d.id) == str(json_id):
            result = d.data
    if not result:
        return "sry, no json found!"

    return jsonify(result)


@app.route('/edit_json', methods=["PUT", "POST"])
def edit_json():
    json_data = request.get_json(force=True)
    json_to_edit_id = json_data['jsonId']
    del json_data['jsonId']
    json_found = False

    for d in data:
        if str(d.id) == str(json_to_edit_id):
            d.data = json_data
            json_found = True

    if json_found:
        return str(json_data)
    else:
        return "sry, no json found!"


@app.route('/delete_json', methods=["GET"])
def delete_json():
    json_id = request.args.get('jsonId')
    json_found = False
    for d in data:
        if str(d.id) == str(json_id):
            data.remove(d)
            json_found = True

    if json_found:
        return "json removed!"
    else:
        return "sry, no json found!"


@app.route('/about', methods=["GET"])
def about():
    return app.send_static_file('about.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
