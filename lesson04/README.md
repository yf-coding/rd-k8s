# Lesson 4.

Build an image with redandant components:
```
$ sudo docker build -t nodeapp:0.0.1 -f Dockerfile_huge .
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
$ sudo docker push  yfrepo/nodeapp:0.0.2

$ sudo docker push  yfrepo/nodeapp:0.0.2
```


```
$ sudo docker image ls
REPOSITORY       TAG       IMAGE ID       CREATED        SIZE
nodeapp          0.0.2     5da945931a31   10 hours ago   161MB
yfrepo/nodeapp   0.0.2     5da945931a31   10 hours ago   161MB
nodeapp          0.0.1     125b0a3721d1   10 hours ago   1.12GB
yfrepo/nodeapp   0.0.1     125b0a3721d1   10 hours ago   1.12GB
```


Link to the docker-hub repo: 
https://hub.docker.com/repository/docker/yfrepo/nodeapp/general


