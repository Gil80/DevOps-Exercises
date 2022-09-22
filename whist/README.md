# Whist
## Description
This project runs a flask app that prints the IP address of the container its running on, and an Nginx webserver that acts as a round-robin load balancer.

The `docker-compose.yml` is configured to run three instances (containers) of the same flask app.

## Usage
1. Clone this repo to your local machine
2. From within the root directory of the project, run `docker compose up --build`
3. Once the environment is up and running, browse to `http://localhost:9090` and you should see the IP address of one of the containers running an instance of flask.
4. Press F5 to see how the round-robin LB directs the request to a different IP/container.


## Issues on my local machine
problem: couldn't start docker daemon: https://appuals.com/cannot-connect-to-the-docker-daemon-at-unix-var-run-docker-sock/
failed solution: systemctl start docker

problem: System has not been booted with systemd as init system (PID 1). Can't operate.
solution: sudo service docker start

# The Assignment
HomeWork IT :
1. Create a private repo on github.
2. Create an app (web app) that prints the local IP to the browser (on HTTP - port 80) Use
any coding language you want.
3. Create a load balancer based on a docker nginx image exposed on port 9090.
4. Create a docker compose that runs 3 instances of the app you created + the load
balancer.
5. Open browser and check http://localhost:9090, verify you see different IP each refresh.