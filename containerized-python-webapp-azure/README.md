# u-btech-demo

## Requirements
Create a web application API using python called: “Bookjobs.”
The application has three controllers:
1. POST: create a new job.
2. GET: list all jobs.
3. DELETE: delete a job.

The app is `app.py` under the `/app` folder.

## Instructions
1. Run the app
2. Use postman to `GET` `http://127.0.0.1:5000/bookjobs`
3. To get a specific ID, use `GET` `http://127.0.0.1:5000/bookjobs/{id}`
4. To `DELETE` a specific ID, use `DELETE` ``http://127.0.0.1:5000/bookjobs/{id}`, and specify in the body the key-value pair to delete in json format.

## Instructions if running containerized app
1. Use the curl_commands.sh file to issue REST API commands for GET/POST/DELETE.
2. Run the container by binding the host port to the container exposed port: `docker run -p 80:5000 -it flask`.
3. Open another shell terminal and then issue the curl commands.
4. The app will run on your browser at `localhost/bookjobs` URL.


    
