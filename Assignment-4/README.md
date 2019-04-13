# Assignment-4:Load Balancing

### To see docker images present
```
sudo docker images
```

### To list all the containers running
```
sudo docker ps
```


### To stop docker container
```
sudo docker stop CONTAINER_ID
```

### To bulid the docker image users
```
sudo docker build -t users:latest .
```


### To run docker users container
```
sudo docker run -p 80:5000 -it users
```


### To run docker users container in deattached mode
```
sudo docker run -d -p 80:5000 -it users
```


### To bulid the docker image acts
```
sudo docker build -t acts:latest .
```


### To run docker acts container
```
sudo docker run -p 80:5000 -it acts
```


### To run docker acts container in deattached mode
```
sudo docker run -d -p 80:5000 -it acts
```


 
