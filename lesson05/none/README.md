# Lesson 5

## None network driver

Creaint containers on None network.
```
docker run -dit --network none --name none1 busybox
a9ca837d4ee76aaf66fc308a124b4128b87b3016dd6ae3def9f25a9038383dd6

$ docker run -dit --network none --name none2 busybox
500d70f1341469905656936b1b529b6144024276b712776ea9b3cac50a74060e

$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED          STATUS          PORTS     NAMES
500d70f13414   busybox   "sh"      3 seconds ago    Up 2 seconds              none2
a9ca837d4ee7   busybox   "sh"      31 seconds ago   Up 30 seconds             none1
```

Inspecting the 'none' network:
```
$ docker network inspect none | jq '.[0].Containers'
{
  "24a2cde08d9b01a851ec668ef8dfd6a2409639479fca317df05a1f64b2c9c8f6": {
    "Name": "none1",
    "EndpointID": "a1fea5beced82a6888d7451931b9e19e246cd87c229c9ebb1f260c9101b671fe",
    "MacAddress": "",
    "IPv4Address": "",
    "IPv6Address": ""
  },
  "fd8cc71c125e5c406518fbdcc23b0071018dc9556ee70bd9bfaddc1a7ab8c4a2": {
    "Name": "none2",
    "EndpointID": "89d8ce0bfaa1cdff9d07209de4b6e64bdbf00842e143f5043e15714042b3fd23",
    "MacAddress": "",
    "IPv4Address": "",
    "IPv6Address": ""
  }
}
```


The containers are fully isolated:
```
$ docker container exec -it none1 ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
```
```
$ docker container exec -it none2 ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
```