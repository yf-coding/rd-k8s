# Lesson 5. Volumes

Create a volume:
```
$ docker volume create vol_lesson5
vol_lesson5
```

Inspect the volume created:
```
$ docker volume ls
DRIVER    VOLUME NAME
local     vol_lesson5


$ docker volume inspect vol_lesson5
[
    {
        "CreatedAt": "2025-02-15T16:55:51Z",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/vol_lesson5/_data",
        "Name": "vol_lesson5",
        "Options": null,
        "Scope": "local"
    }
]
```

Creating containers with columes attached:
```
$ docker container run -dit --name app1 -v vol_lesson5:/data busybox

$ docker container run -dit --name app2 -v vol_lesson5:/data busybox

$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED          STATUS          PORTS     NAMES
63238fc48c38   busybox   "sh"      4 seconds ago    Up 3 seconds              app2
6c78a58baccb   busybox   "sh"      11 seconds ago   Up 11 seconds             app1
```

Inspecting the containers on mounted volume settings:
```
$ docker container inspect app1 | jq '.[0].Mounts'
[
  {
    "Type": "volume",
    "Name": "vol_lesson5",
    "Source": "/var/lib/docker/volumes/vol_lesson5/_data",
    "Destination": "/data",
    "Driver": "local",
    "Mode": "z",
    "RW": true,
    "Propagation": ""
  }
]

$ docker container inspect app2 | jq '.[0].Mounts'
[
  {
    "Type": "volume",
    "Name": "vol_lesson5",
    "Source": "/var/lib/docker/volumes/vol_lesson5/_data",
    "Destination": "/data",
    "Driver": "local",
    "Mode": "z",
    "RW": true,
    "Propagation": ""
  }
]
```

Playing with the volume, some content within it and the content visibility with the containers.

Volume's folder is empty:
```
$ echo $(docker volume inspect vol_lesson5 | jq -r '.[0].Mountpoint')
/var/lib/docker/volumes/vol_lesson5/_data

$ sudo ls -la $(docker volume inspect vol_lesson5 | jq -r '.[0].Mountpoint' )
total 8
drwxr-xr-x 2 root root 4096 Feb 15 17:14 .
drwx-----x 3 root root 4096 Feb 15 16:55 ..
```


Creating a file `file1.txt` in the folder /data/ which is mounted volume in the container `app1`:
```
$ docker container exec -it app1 touch /data/file1.txt

$ docker container exec -it app1 ls -la /data/
total 8
drwxr-xr-x    2 root     root          4096 Feb 15 17:26 .
drwxr-xr-x    1 root     root          4096 Feb 15 16:56 ..
-rw-r--r--    1 root     root             0 Feb 15 17:26 file1.txt
```

Checking if the volume folder contains the file:
```
$ sudo ls -la $(docker volume inspect vol_lesson5 | jq -r '.[0].Mountpoint')
total 8
drwxr-xr-x 2 root root 4096 Feb 15 17:26 .
drwx-----x 3 root root 4096 Feb 15 16:55 ..
-rw-r--r-- 1 root root    0 Feb 15 17:26 file1.txt
```

Checking if the container `app2` can see the same data in the mounted volume:
```
$ docker container exec -it app2 ls -la /data/
total 8
drwxr-xr-x    2 root     root          4096 Feb 15 17:26 .
drwxr-xr-x    1 root     root          4096 Feb 15 16:57 ..
-rw-r--r--    1 root     root             0 Feb 15 17:26 file1.txt
```

Creating one more file `file2.txt` in the `/data` folder in the continer `app2`:
```
$ docker container exec -it app2 touch /data/file2.txt

$ docker container exec -it app2 ls -la /data/
total 8
drwxr-xr-x    2 root     root          4096 Feb 15 17:32 .
drwxr-xr-x    1 root     root          4096 Feb 15 16:57 ..
-rw-r--r--    1 root     root             0 Feb 15 17:26 file1.txt
-rw-r--r--    1 root     root             0 Feb 15 17:32 file2.txt
```

Checking if the container `app1` can see the same data in the mounted volume:
```
$ docker container exec -it app1 ls -la /data/
total 8
drwxr-xr-x    2 root     root          4096 Feb 15 17:32 .
drwxr-xr-x    1 root     root          4096 Feb 15 16:56 ..
-rw-r--r--    1 root     root             0 Feb 15 17:26 file1.txt
-rw-r--r--    1 root     root             0 Feb 15 17:32 file2.txt
```

Checking the volume folder:
```
$ sudo ls -la $(docker volume inspect vol_lesson5 | jq -r '.[0].Mountpoint')
total 8
drwxr-xr-x 2 root root 4096 Feb 15 17:32 .
drwx-----x 3 root root 4096 Feb 15 16:55 ..
-rw-r--r-- 1 root root    0 Feb 15 17:26 file1.txt
-rw-r--r-- 1 root root    0 Feb 15 17:32 file2.txt
```

Removing the files in the volume:
```
$ sudo rm -rf $(docker volume inspect vol_lesson5 | jq -r '.[0].Mountpoint' )/*

$ sudo ls -la /var/lib/docker/volumes/vol_lesson5/_data
total 8
drwxr-xr-x 2 root root 4096 Feb 15 17:40 .
drwx-----x 3 root root 4096 Feb 15 16:55 ..
```

Checking if the containers see the last changes:
```
$ docker container exec -it app1 ls -la /data/
total 8
drwxr-xr-x    2 root     root          4096 Feb 15 17:40 .
drwxr-xr-x    1 root     root          4096 Feb 15 16:56 ..

$ docker container exec -it app2 ls -la /data/
total 8
drwxr-xr-x    2 root     root          4096 Feb 15 17:40 .
drwxr-xr-x    1 root     root          4096 Feb 15 16:57 ..
```

Trying to remove the volume in ise:
```
$ docker volume rm vol_lesson5
Error response from daemon: remove vol_lesson5: volume is in use - [6c78a58baccbc6e3bc95aa92ebd2c9432ef5e2134b083c06d604fc65a1c2c919, 63238fc48c382f7db8198f8d0aa0b4701750ae994bf2aa09c1dec296e48b029d]
```

Let'create a file in the volume mounted to the running contained and after that stop the containers and finally try to remove the volume:
```
$ docker container exec -it app1 touch /data/file.txt

$ docker container stop $(docker ps -aq)

$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

$ docker volume rm vol_lesson5
Error response from daemon: remove vol_lesson5: volume is in use - [6c78a58baccbc6e3bc95aa92ebd2c9432ef5e2134b083c06d604fc65a1c2c919, 63238fc48c382f7db8198f8d0aa0b4701750ae994bf2aa09c1dec296e48b029d]
```

Now, Let's remove the containers and try to remove the volume:
```
$ docker rm $(docker ps -aq)
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

$ echo  $(docker volume inspect vol_lesson5 | jq -r '.[0].Mountpoint')
/var/lib/docker/volumes/vol_lesson5/_data

$ sudo ls -la $(docker volume inspect vol_lesson5 | jq -r '.[0].Mountpoint')
total 8
drwxr-xr-x 2 root root 4096 Feb 15 17:57 .
drwx-----x 3 root root 4096 Feb 15 16:55 ..
-rw-r--r-- 1 root root    0 Feb 15 17:57 file.txt
```

The volume stil keeps the data.

Remove the volume not beeing used:
```
$ docker volume ls
DRIVER    VOLUME NAME
local     vol_lesson5

$ docker volume prune -f -a
Deleted Volumes:
vol_lesson5

Total reclaimed space: 0B

$ docker volume ls
DRIVER    VOLUME NAME
```