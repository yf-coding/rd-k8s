# Lesson 5

Initial network list:
```
$ docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
ca6318355302   bridge    bridge    local
8d7d7c44c7dd   host      host      local
549ae839ef61   none      null      local
```

## Bridge networking

### Default bridge network

Running containers on a default (bridge) network
```
$ docker run -dit --name busybox1 busybox
6b25cea56527196b557ee2425e1b64dcc883ac17f44897824a15a53799bacaf0

$ docker run -dit --name busybox2 busybox
ca96ac643931359e376118f22185bc42bf6d16b7f3036301791937f89b040efc
```

Inspecting a default network on containers attached:
```
$ docker network inspect  bridge | jq '.[0].Containers'
{
  "6b25cea56527196b557ee2425e1b64dcc883ac17f44897824a15a53799bacaf0": {
    "Name": "busybox1",
    "EndpointID": "fbfb24e3ce4fa2d362181ec6a5bee4a1c62f7c2ce231f31f9e3e6ae8dbb92384",
    "MacAddress": "02:42:ac:11:00:02",
    "IPv4Address": "172.17.0.2/16",
    "IPv6Address": ""
  },
  "ca96ac643931359e376118f22185bc42bf6d16b7f3036301791937f89b040efc": {
    "Name": "busybox2",
    "EndpointID": "6b5ecbca6e8ced6b4904dfd61d0c078850701d72263a2ccbdbecd02933e37214",
    "MacAddress": "02:42:ac:11:00:03",
    "IPv4Address": "172.17.0.3/16",
    "IPv6Address": ""
  }
}
```

Reaching a container busybox2 by its IP addr 172.17.0.3:
```
$ docker container exec -it busybox1 ping -c2 172.17.0.3
PING 172.17.0.3 (172.17.0.3): 56 data bytes
64 bytes from 172.17.0.3: seq=0 ttl=64 time=0.174 ms
64 bytes from 172.17.0.3: seq=1 ttl=64 time=0.087 ms

--- 172.17.0.3 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.087/0.130/0.174 ms
```


### Custom brdge network

Creating a bridge network
```
$ docker network create -d bridge rd-bridge
dd161d59678cb6bcf1763e27ccb6bd15225a4904f27ac6fd463962a349d515fb

$ docker network ls
NETWORK ID     NAME        DRIVER    SCOPE
ca6318355302   bridge      bridge    local
8d7d7c44c7dd   host        host      local
549ae839ef61   none        null      local
dd161d59678c   rd-bridge   bridge    local
```
Inspecting the `rd-bridge` network just created:
```
$ docker network inspect  rd-bridge
[
    {
        "Name": "rd-bridge",
        "Id": "dd161d59678cb6bcf1763e27ccb6bd15225a4904f27ac6fd463962a349d515fb",
        "Created": "2025-02-15T12:24:30.06986368Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        ...
```


Running containers with hostnames on the custom `rd-bridge` network:
```
$ docker container run -d -p8001:80 --network rd-bridge --name nginx1 -h nginx1  nginx
d6d5c452fd009c27e7d0741dd0e852f00ecbb98db213a38382caf630db0d4099

$ docker container run -d -p8002:80 --network rd-bridge --name nginx2 -h nginx1 nginx
13a657a57a81efb49578fa150872ec8d95e2cbb886f4109af4beff5b687dee6e
```

Check the network/containers attached
```
$ docker network inspect  rd-bridge | jq '.[0].Containers'
{
  "13a657a57a81efb49578fa150872ec8d95e2cbb886f4109af4beff5b687dee6e": {
    "Name": "nginx2",
    "EndpointID": "0b3a4f83afc8aa216a8c43be4df0b8a149b08402bb3e966f64fb04ba8f40cb40",
    "MacAddress": "02:42:ac:12:00:03",
    "IPv4Address": "172.18.0.3/16",
    "IPv6Address": ""
  },
  "d6d5c452fd009c27e7d0741dd0e852f00ecbb98db213a38382caf630db0d4099": {
    "Name": "nginx1",
    "EndpointID": "63587b8a4bfe886ea486c71487d5d78283ff8dd6c7e19d463bd1e41d8d637b59",
    "MacAddress": "02:42:ac:12:00:02",
    "IPv4Address": "172.18.0.2/16",
    "IPv6Address": ""
  }
}
```

The container `nginx2` is reachable by its IP addr and its DNS name:
```
$ docker container exec -it nginx1 ping -c2 172.18.0.3
PING 172.18.0.3 (172.18.0.3) 56(84) bytes of data.
64 bytes from 172.18.0.3: icmp_seq=1 ttl=64 time=0.262 ms
64 bytes from 172.18.0.3: icmp_seq=2 ttl=64 time=0.078 ms

--- 172.18.0.3 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1060ms
rtt min/avg/max/mdev = 0.078/0.170/0.262/0.092 ms
```

```
$ docker container exec -it nginx1 ping -c2 nginx2
PING nginx2 (172.18.0.2) 56(84) bytes of data.
64 bytes from nginx2.rd-bridge (172.18.0.2): icmp_seq=1 ttl=64 time=0.081 ms
64 bytes from nginx2.rd-bridge (172.18.0.2): icmp_seq=2 ttl=64 time=0.604 ms

--- nginx2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1003ms
rtt min/avg/max/mdev = 0.081/0.342/0.604/0.261 ms
```

Containers on the bridged network are reachable both from the local network and outside its network:

Local `rd-bridge` network:
```
$ curl 172.18.0.1:8001
<!DOCTYPE html>
<html>
...
```
Docker host network:
```
$ curl localhost:8001
<!DOCTYPE html>
<html>
...
``` 
Local home network:
```
$ curl 192.168.0.110:8001
<!DOCTYPE html>
<html>
...
``` 