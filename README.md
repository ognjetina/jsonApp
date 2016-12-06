# jsonApp

This app was made to hould our json data for app tests or something similar on our local server.
Take in mind that jsons are in memory so if the server shuts down jsons will be lost!

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

Usage:
    <ul>
        <li>You can take a look at all jsons at link:  <u>https://localhost:5000/</u></li>
        <li>
            <p>You can <strong>add</strong> your json by sending POST or PUT method at <u> https://localhost:5000/add_json</u> url with your
                json and server
                will tell you your <u>json id.</u></p></li>
        <li>
            <p>You can <strong>edit</strong> your json by sending POST or PUT method at <u>https://localhost:5000/edit_json</u> with your new
                json data.
                <br>Just add "jsonId" field to your new json with id of json you are editing (no worries jsonId field
                will not be added).</p>
        </li>
        <li>
            <p>You can <strong>delete</strong> your json by sending GET method to <u>https://localhost:5000/delete_json</u> with parameter
                jsonId.</p>
        </li>
        <li>
            <p>You can <strong>get</strong> your json by sending GET method to <u>https://localhost:5000/get_json</u> with parameter jsonId.
            </p>
     </ul>
