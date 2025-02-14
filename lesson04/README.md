# Lesson 4.
## Ubuntu based Dockerfile:
```
$ cat Dockerfile_huge
FROM node:20.18.3

WORKDIR /app
COPY package.json server.js /app/
RUN npm install
EXPOSE 4000

```
Build an image with redandant components:
```
$ sudo docker build -t nodeapp:0.0.1 -f Dockerfile_huge .
```

## Optimization of a docker image with multistage build
```
$ cat Dockerfile_multistage
FROM node:20.18.3 as build
WORKDIR /app
COPY package.json server.js /app/
RUN npm install

FROM node:20.18.3-alpine as main
COPY --from=build /app /
EXPOSE 4000
ENTRYPOINT ["node", "server.js"]
```
Build a minimized image with multistage build:
```
$ sudo docker build -t nodeapp:0.0.2 -f Dockerfile_multistage .
```

Compare images just built:
```
$ sudo docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
nodeapp      0.0.2     5da945931a31   10 hours ago   161MB
nodeapp      0.0.1     125b0a3721d1   10 hours ago   1.12GB
```

```
$ sudo docker login -u yfrepo
```
Tagging images to push into a docker registry:
```  
$ sudo docker tag nodeapp:0.0.1 yfrepo/nodeapp:0.0.1
 
$ sudo docker push  yfrepo/nodeapp:0.0.1
```

```
$ sudo docker tag nodeapp:0.0.2 yfrepo/nodeapp:0.0.2

$ sudo docker push  yfrepo/nodeapp:0.0.2
```
Link to the docker-hub repo: 
https://hub.docker.com/r/yfrepo/nodeapp/tags




# Verification

Removing local images:
```
$ sudo docker rmi -f $(sudo docker image ls -q)
$ sudo docker image ls
REPOSITORY   TAG       IMAGE ID   CREATED   SIZE
```
Pulling images:
```
$ sudo docker pull yfrepo/nodeapp:0.0.1
0.0.1: Pulling from yfrepo/nodeapp
...

$ sudo docker pull yfrepo/nodeapp:0.0.2
0.0.2: Pulling from yfrepo/nodeapp
1f3e46996e29: Already exists                                                                                                                                                                             
8e453ffab4f9: Already exists                                                                                                                                                                             
f20b88d69c85: Already exists                                                                                                                                                                             
7daf61b3a521: Already exists                                                                                                                                                                             
60b87b0c9faa: Already exists                                                                                                                                                                             
Digest: sha256:3d485adc54280c4ac8c579f44ac77c1e612737e5a677333506d6b822e6a60f9c
Status: Downloaded newer image for yfrepo/nodeapp:0.0.2
docker.io/yfrepo/nodeapp:0.0.2


$ sudo docker images
REPOSITORY       TAG       IMAGE ID       CREATED        SIZE
yfrepo/nodeapp   0.0.2     5da945931a31   23 hours ago   161MB
yfrepo/nodeapp   0.0.1     125b0a3721d1   23 hours ago   1.12GB
```

Running containers:
```
$ sudo docker run -d -p4001:4000 --name nodeapp_hude yfrepo/nodeapp:0.0.1
43293d0803b68a1cdc092ffae9d0c84a40511c0f38fc2cd0ebc446371596e020

$ sudo docker run -d -p4002:4000 --name nodeapp_small yfrepo/nodeapp:0.0.2
51cd03e4ad77e90e8b56a4d4578ed85596d39d3b59d8a75f319929efb641abb7

$ sudo docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS                                         NAMES
51cd03e4ad77   yfrepo/nodeapp:0.0.2   "docker-entrypoint.s…"   9 seconds ago    Up 8 seconds    0.0.0.0:4002->4000/tcp, [::]:4002->4000/tcp   nodeapp_small
43293d0803b6   yfrepo/nodeapp:0.0.1   "docker-entrypoint.s…"   23 seconds ago   Up 22 seconds   0.0.0.0:4001->4000/tcp, [::]:4001->4000/tcp   nodeapp_hude
```

Testing the containers:
```
$ curl 192.168.0.110:4001
Hello World

$ curl 192.168.0.110:4002
Hello World
```

