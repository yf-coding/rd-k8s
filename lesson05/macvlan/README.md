# Lesson 5
## macvlan network

### `macvlan` with dynamic IP addressing

Creating a `macvlan` type network:
```
$ docker network create -d macvlan \
     --subnet=192.168.0.0/24 \
     --gateway=192.168.0.1 \
     -o parent=enp0s3  rd-macvlan1

7c8fb9d5ac623f389bb255f6a8138c36ebec1a59517f00ae6bb157c3f68f3afc
```

```
$ docker network inspect rd-macvlan1
[
    {
        "Name": "rd-macvlan1",
        "Id": "7c8fb9d5ac623f389bb255f6a8138c36ebec1a59517f00ae6bb157c3f68f3afc",
        "Created": "2025-02-15T15:34:29.301867692Z",
        "Scope": "local",
        "Driver": "macvlan",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "192.168.0.0/24",
                    "Gateway": "192.168.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {},
        "Options": {
            "parent": "enp0s3"
        },
        "Labels": {}
    }
]
```

Running containers on the `rd-macvlan1` network just created:
```
$ docker container run -dit --name macvlan1 --network rd-macvlan1 busybox
e6aee6606fe585b61184f189384f2d41cab2cf48e2e57dfaf509e88fb2c79a3c

$ docker container run -dit --name macvlan2 --network rd-macvlan1 busybox
8d93cfa1cf1ddb8cebe7b1e612d2fe910b800be816329a5b2e17c442a2a962a0
```

Inspecting the `rd-macvlan1` network on containers attached:
```
$ docker network inspect rd-macvlan1 | jq '.[0].Containers'
{
  "8d93cfa1cf1ddb8cebe7b1e612d2fe910b800be816329a5b2e17c442a2a962a0": {
    "Name": "macvlan2",
    "EndpointID": "d57c03f68568b157ff524945e3fb784d864fc452343094e12214030b216ef37c",
    "MacAddress": "02:42:c0:a8:00:03",
    "IPv4Address": "192.168.0.3/24",
    "IPv6Address": ""
  },
  "e6aee6606fe585b61184f189384f2d41cab2cf48e2e57dfaf509e88fb2c79a3c": {
    "Name": "macvlan1",
    "EndpointID": "cb6023ddfb3b7bfe716c5304ef149dc1a6c6ad78a2f33258ce5ebedc7c5aa638",
    "MacAddress": "02:42:c0:a8:00:02",
    "IPv4Address": "192.168.0.2/24",
    "IPv6Address": ""
  }
}
```

Checking IP addresses in the containers:
```
$ docker exec -it macvlan1 ifconfig eth0
eth0      Link encap:Ethernet  HWaddr 02:42:C0:A8:00:02
          inet addr:192.168.0.2  Bcast:192.168.0.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1028 errors:0 dropped:0 overruns:0 frame:0
          TX packets:4 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:174732 (170.6 KiB)  TX bytes:280 (280.0 B)

$ docker exec -it macvlan2 ifconfig eth0
eth0      Link encap:Ethernet  HWaddr 02:42:C0:A8:00:03
          inet addr:192.168.0.3  Bcast:192.168.0.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:978 errors:0 dropped:0 overruns:0 frame:0
          TX packets:4 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:169282 (165.3 KiB)  TX bytes:280 (280.0 B)
```


Reaching the container `macvlan1` from the local network:
```
$ ping -c2 192.168.0.2
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
From 192.168.0.110 icmp_seq=1 Destination Host Unreachable
From 192.168.0.110 icmp_seq=2 Destination Host Unreachable

--- 192.168.0.2 ping statistics ---
2 packets transmitted, 0 received, +2 errors, 100% packet loss, time 1080ms
pipe 2
```

Testing connection to the container `macvlan2` (`192.168.0.3`) from the container `macvlan1` (`192.168.0.2`):
```
$ docker container exec -it macvlan1 ping -c2 192.168.0.3
PING 192.168.0.3 (192.168.0.3): 56 data bytes
64 bytes from 192.168.0.3: seq=0 ttl=64 time=0.209 ms
64 bytes from 192.168.0.3: seq=1 ttl=64 time=0.057 ms

--- 192.168.0.3 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.057/0.133/0.209 ms
```


### `macvlan` with static IP addressing

```
$ docker container run -dit \
     --name macvlan200 \
     --network rd-macvlan2 \
     --ip 192.168.0.200 busybox

4dbce0f5c94d293c74b8abfd6ded7b647a552ab7bed30aa43de8a5d81512b62f


$ docker container run -dit \
     --name macvlan201 \
     --network rd-macvlan2 \
     --ip 192.168.0.201 busybox

8235f7a2c94ee40ea6bd1e4c7d07609b9f6a7f74dc77b6c24afb9941e6056e62


$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED          STATUS          PORTS     NAMES
8235f7a2c94e   busybox   "sh"      4 seconds ago    Up 3 seconds              macvlan201
4dbce0f5c94d   busybox   "sh"      15 seconds ago   Up 14 seconds             macvlan200
```

Testing a connection to the containers from the local network:
```
$ ping -c2  192.168.0.200
PING 192.168.0.200 (192.168.0.200) 56(84) bytes of data.
From 192.168.0.110 icmp_seq=1 Destination Host Unreachable
From 192.168.0.110 icmp_seq=2 Destination Host Unreachable

--- 192.168.0.200 ping statistics ---
2 packets transmitted, 0 received, +2 errors, 100% packet loss, time 1055ms
pipe 2

$ ping -c2  192.168.0.201
PING 192.168.0.201 (192.168.0.201) 56(84) bytes of data.
From 192.168.0.110 icmp_seq=1 Destination Host Unreachable
From 192.168.0.110 icmp_seq=2 Destination Host Unreachable

--- 192.168.0.201 ping statistics ---
2 packets transmitted, 0 received, +2 errors, 100% packet loss, time 1010ms
pipe 2
```

Testing a connection between the containers:
```
$ docker container exec -it macvlan201 ping -c2 192.168.0.201
PING 192.168.0.201 (192.168.0.201): 56 data bytes
64 bytes from 192.168.0.201: seq=0 ttl=64 time=0.271 ms
64 bytes from 192.168.0.201: seq=1 ttl=64 time=0.050 ms

--- 192.168.0.201 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.050/0.160/0.271 ms
```