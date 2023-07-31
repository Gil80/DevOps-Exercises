1. run the app.py locally to validate it running and exposing IP address of the flask server on port 5000
2. build a container from the dockerfile using `docker build -t flask .` 
3. run the container using `docker run -it -u gil -p 5000:5000 flask bash`
4. within the bash of the running container, run: `python3 app.py`
5. the flask app should run on `http://127.0.0.1:5000` click on the URL and validate the browser prints "172.17.0.2"