# Lesson 5

## Host network


Creating a container on a host network.
Port forwarding doesn't have effect here.
```
docker container run -d --name host_web --network host nginx
```

Inspecting the `host` network:
```
$ docker network inspect host
[
    {
        "Name": "host",
        "Id": "8d7d7c44c7dd02d3df7e0683e0a123baef313b3e242bac9c34a7bfb2c5bb0eb3",
        "Created": "2025-01-30T19:29:13.213203793Z",
        "Scope": "local",
        "Driver": "host",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": null
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "56f979df09d095fd2d3c8ada4ac6ec9aefd529b9f0f9949fadb5c1e4726bc494": {
                "Name": "host_web",
                "EndpointID": "944d509d9af91710013dae4db7e2c5c325f3963d35606240d9a8f0cc5a7795a0",
                "MacAddress": "",
                "IPv4Address": "",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```
The container does not have any IP address assigned. It shares the IP with the Docker host machine.

Testing the conatiner:
```
$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                                     NAMES
56f979df09d0   nginx     "/docker-entrypoint.…"   24 minutes ago   Up 24 minutes                                             host_web

$ curl localhost
<!DOCTYPE html>
<html>
<head>
```

Let's try to run a container on the `host` network exposing the same port **80**
```
$ docker container run -d --name host_web3 --network host httpd
```

It's failed on the start up:
```
$ docker logs host_web3
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 127.0.1.1. Set the 'ServerName' directive globally to suppress this message
(98)Address already in use: AH00072: make_sock: could not bind to address [::]:80
(98)Address already in use: AH00072: make_sock: could not bind to address 0.0.0.0:80
no listening sockets available, shutting down
AH00015: Unable to open logs
```

