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