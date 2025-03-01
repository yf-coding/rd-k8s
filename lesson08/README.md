# Lesson 8

```
# Creating a namespace
$ microk8s.kubectl create namespace lesson8
namespace/lesson8 created

# Applying the deployment configs (Crating a deployment and Deploying services)
$ microk8s.kubectl apply -f deployment.yaml -n lesson8
deployment.apps/flask-app created
service/flask-app-service created

# Checking pods just created
$ microk8s.kubectl get pods -n lesson8
NAME                         READY   STATUS    RESTARTS   AGE
flask-app-76f48b5bbd-hhnnw   1/1     Running   0          26s
flask-app-76f48b5bbd-kcctd   1/1     Running   0          27s
flask-app-76f48b5bbd-wnsjm   1/1     Running   0          27s
flask-app-76f48b5bbd-wtsvz   1/1     Running   0          26s
flask-app-76f48b5bbd-xn8nh   1/1     Running   0          27s

# Checking the service running
$ microk8s.kubectl get services -n lesson8
NAME                TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
flask-app-service   NodePort   10.152.183.253   <none>        80:30891/TCP   37s

# Checking the service resp, each time another replica sends the responce:
$ curl 10.152.183.253
{"ip_addr":"['10.1.77.57']","message":"Hello from cluster <flask-app-76f48b5bbd-hhnnw>"}

$ curl 10.152.183.253
{"ip_addr":"['10.1.77.56']","message":"Hello from cluster <flask-app-76f48b5bbd-kcctd>"}

$ curl 10.152.183.253
{"ip_addr":"['10.1.77.58']","message":"Hello from cluster <flask-app-76f48b5bbd-wnsjm>"}
```
