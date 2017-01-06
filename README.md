# jsonApp

This is a RESTful app that holds json files in memory.<br>
Keep in mind that if you stop the server all jsons are lost.

Run:
  <ul>
  <li>
  Start on local
  ```{engine='sh}
  git clone https://github.com/ognjetina/jsonApp.git
  cd jsonApp
  virtualenv venvJsonApp
  . /venvJsonApp/bin/activate
  pip install -r requirements.txt
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

Add your json:

Make a POST request with your json file on: http://localhost:5000/json
Json has to contain jsonId field with id you are going to use to find edit or delete your json.
jsonId field will not be saved in your json.
                    
If you wont to protect your json with password your json has to contain jsonPassword field.
jsonPassword will not be saved in your json, but you wont be able to delete or update your json
without it so remember the password.
If everything is right your json will be stored with its ID and server will respond with http status
code 201.
         
Get your json:

Make a GET request with argument jsonId on: http://localhost:5000/json
                 
example: http://localhost:5000/json?jsonId=1
Server will return json if json exists.

       
Change your json:
            
If not password protected:
Make a PUT request with your new json data and add jsonId to your json:
http://localhost:5000/json
               
example: send PUT with json: 
{"firstName":"Peter","jsonId":"2"}
and server will remove jsonId field and update your json.

If password protected:
Make a PUT request with your new json data and add jsonId and jsonPassword to your json:
http://localhost:5000/json
                  
example: send PUT with json: 
{"firstName":"Peter","jsonId":"2","jsonPassword:"myPasswordIsEpic"}
and server will remove jsonId amd jsonPassword fields and update your json if your password is correct.
    
Delete your json:
           
If not password protected:
Make a DELETE request with argument jsonId on: http://localhost:5000/json

example: send DELETE to http://localhost:5000/json?jsonId=1
Server will delete json with id 1.

If password protected:
Make a DELETE request with argument jsonId and jsonPassword on: http://localhost:5000/json
example: send DELETE to http://localhost:5000/json?jsonId=1&jsonPassword=password
Server will delete json with id 1.
        
    
