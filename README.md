# jsonApp

This is a RESTful app that holds json files in memory.<br>
Keep in mind that if you stop the server all jsons are lost.

Run:
  <ul>
  <li>
  Start on local
  ```{engine='sh}
  git clone https://github.com/ognjetina/jsonApp.git
  python app.py
  ```
  </li>
  <li>
    Start on docker
  ```{engine='sh}
  git clone https://github.com/ognjetina/jsonApp.git
  docker build -t json-app:latest .
  docker run -d -p 5000:5000 json-app
  ```
  </li>
  </ul>

Use:
  <ul>
        <li>
            Add your json:
            <ul>
                <li>
                    Make a POST request with your json file on: http://localhost:5000/json
                    <br><br>
                    Your json will be stored with its unique ID and server will respond with http status code 201.
                </li>
            </ul>
        </li>
        <br>
        <li>
            Get your json:
            <ul>
                <li>
                    Make a GET request with argument jsonId on: http://localhost:5000/json
                    <br><br>
                    example: http://localhost:5000/json?jsonId=1<br>
                    Server will return json if json exists.
                </li>
            </ul>
        </li>
        <br>
        <li>
            Change your json:
            <ul>
                <li>
                    Make a PUT request with your new json data and add jsonId at the end of your json on:
                    http://localhost:5000/json
                    <br><br>
                    example: send PUT with json: <br>
                    {"firstName":"Peter","jsonId":"2"}<br>
                    and server will remove jsonId field and update your json.
                </li>
            </ul>
        </li>
        <br>
        <li>
            Delete your json:
            <ul>
                <li>
                    Make a DELETE request with argument jsonId on: http://localhost:5000/json
                    <br><br>
                    example: send DELETE to http://localhost:5000/json?jsonId=1<br>
                    Server will delete json with id 1.
                </li>
            </ul>
        </li>
    </ul>