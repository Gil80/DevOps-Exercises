# Construct an autoscaling solution on GKE for a node application


## Requirements

1. Mongodb replicaset installed on 3 **instances (not gke)** - master, slave & arbiter
2. Nodeapp code should be updated to use the replicaset instead of a single server
3. Nodeapp should be deployed on GKE with autoscaling and should scale from 2 to 10 pods.
4. Nodeapp should be exposed with an ingress with http and https (self-signed certificate can be used for https)

### System Illustration
<img src="https://i.ibb.co/6PQ1Qy2/image-20211209153401680.png" alt="image-20211209153401680" border="0">



## MongoDB Replicaset on VMs

<img src="https://i.ibb.co/197BFm7/image-20211209153514150.png" alt="image-20211209153514150" border="0">


1. Created 3 VM’s and read what is the replica set meaning - https://docs.mongodb.com/manual/core/replica-set-architecture-three-members/

2. Attached an SSD as a standard procedure when working with stateful VM’s.

3. Set a default mongoDB port to be used for the VM’s

4. Disabled THP - https://docs.mongodb.com/manual/tutorial/transparent-huge-pages/

5. Established SSH connection using external terminal https://cloud.google.com/compute/docs/instances/connecting-advanced?authuser=1

6. Installing [mongoDB](https://docs.mongodb.com/manual/administration/install-on-linux/)

7. Improve ulimit (https://docs.mongodb.com/manual/reference/ulimit/)

8. Configured mongo.conf

9. Replica set name: **myReplica**

10. VM mapping with internal IP

11. Initiated DB with admin role

12. Created a DB admin user U: gil P: 123!@#

13. Created a DB app user. U: webapp P: webapp123

14. Logging in: `$ mongosh –u gil`
    
15. After setting up primary and secondary, I encountered an error:

16. MongoServerError: Reconfig attempted to install a config that would change the implicit default write concern. Use the setDefaultRWConcern command to set a cluster-wide write concern and try the reconfig again.

17. I used this manual to rectify the issue: [https://docs.mongodb.com/manual/reference/command/setDefaultRWConcern/#mongodb-dbcommand-dbcmd.setDefaultRWConcern](#mongodb-dbcommand-dbcmd.setDefaultRWConcern)



*starting point source:* https://blog.antariksh.dev/deploying-mongodb-replica-set-on-google-cloud-platform-ck9sl0vy800xx6es1o8daz9we




## Nodeapp code should be updated to use the replicaset instead of a single server



1. Editing connection string in **node.js** based on https://docs.mongodb.com/manual/reference/connection-string/
2. Creating the db using command: `use docker-node-mongo`
3. Creating a dockerfile to build a docker image using node:lts as base image
4. Had some trouble figuring out how to write the file. Eventually I used the following guides:
   - https://nodejs.org/en/docs/guides/nodejs-docker-webapp/
   - https://buddy.works/guides/how-dockerize-node-application
   - https://snyk.io/blog/10-best-practices-to-containerize-nodejs-web-applications-with-docker/
   - https://expressjs.com/en/starter/installing.html
5. Encountered an error when trying to run `$ node nodeapp.js` and fixed the part of the code to point at line 19. `const Item = require('./models/item.js');  //./models/Item`. **This is not something I'm too sure about. It seems that the app isn't working properly after my supposedly fix.**
6. Had an error when trying to run the app and after some research: https://exerror.com/npm-err-missing-script-start/




## Nodeapp should be deployed on GKE with autoscaling and should scale from 2 to 10 pods.



1. Enable access to APIs

2. Provided my CC details to enable GCR at [gcr.io]()

3. Created a Dockerfile to create an image

   1. Ran the container locally
   2. Installed dependencies
   3. Copied **package.json** and **package-lock.json t**o my host machine
   4. Built the container again to make sure it's running before pushing to Dockerhub

4. Pushed the image to Docker HUB on my personal account. `docker pull gil80/node-docker` to download the image.

5. Installed Google Cloud SDK.

6. Pushed the image from Dockerhub to GCR.

7. Using this as a source: https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app

8. Used this source to figure out how to deploy the app using K8s: https://testdriven.io/blog/deploying-a-node-app-to-google-cloud-with-kubernetes/#google-cloud-setup

   1. Created a **deployment.yaml** file
   2. Ran `kubectl apply -f deployment.yaml`

9. Scaling via command: `kubectl autoscale deployment nodeapp --cpu-percent=50 --min=2 --max=10`

10. Source: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/

11. Validating: `kubectl get hpa`

12. Created load balancer to expose IP: `kubectl get service nodes`

13. I used `kubectl exec -it nodeapp-765dd7cd45-k4lx9 /bin/bash `to connect to the pod

14. pinged all the vm's using their DNS to validate communication

15. ssh to pod, install mongo shell on the pod - https://docs.mongodb.com/mongodb-shell/install/

16. Use the following command to create a `webapp` 

    ```
    user:db.getUsers();
    
    use docker-node-mongo
    db.createUser(
      {
        user: "webapp",
        pwd:  "webapp123",
        roles: [ { role: "readWrite", db: "docker-node-mongo" },
                 { role: "read", db: "reporting" } ]
      }
    )
    ```

17. Ran `kubectl logs nodeapp-765dd7cd45-k4lx9` to check logs:

    ```nodeapp.js@1.0.0 start
    node nodeapp.js
    Server running...
    MongoDB Connected
    ```

18. grab external IP:  `kubectl get service node`




## Nodeapp should be exposed with an ingress with http and https (self-signed certificate can be used for https)


1. Created an ingress rule using GCP GUI
2. Tested the app at http://35.226.223.59/
3. I tried to insert values to the DB but they are not showing. 



This is where I tried to tackle two problems:

1. Why am I not seeing data from the node app? Or do I understand what the app suppose to do?
2. Getting HTTPS certificate



### Problem 1:

1. I thought that code I changed at line 19 on **nodeapp.js** broke the app so I tried reverting to the original code. `const Item = require('/node/models/Item');`
2. I rebuilt the image and ran the app and this is the error I get:

```js
Error: Cannot find module '/node/models/Item'
Require stack:
- /usr/src/app/nodeapp.js
    at Function.Module._resolveFilename (node:internal/modules/cjs/loader:933:15)
    at Function.Module._load (node:internal/modules/cjs/loader:778:27)
    at Module.require (node:internal/modules/cjs/loader:1005:19)
    at require (node:internal/modules/cjs/helpers:102:18)
    at Object.<anonymous> (/usr/src/app/nodeapp.js:19:14)
    at Module._compile (node:internal/modules/cjs/loader:1101:14)
    at Object.Module._extensions..js (node:internal/modules/cjs/loader:1153:10)
    at Module.load (node:internal/modules/cjs/loader:981:32)
    at Function.Module._load (node:internal/modules/cjs/loader:822:12)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:81:12) {
  code: 'MODULE_NOT_FOUND',
  requireStack: [ '/usr/src/app/nodeapp.js' ]
```


--EOF--




