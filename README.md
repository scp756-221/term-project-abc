[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7281378&assignment_repo_type=AssignmentRepo)

# SFU CMPT756 Term Project 
This is the repo maintained by team-abc for the CMPT756 final project

Our primary goal is to implement a playlist microservice in addition to S1 (user) and S2 (music) services. It contains a new database table and a series of the corresponding APIs to manipulate data. Please see the architecture for our microservices below. 

![mircroservice achitecture](https://user-images.githubusercontent.com/39822436/162517769-de65a5f9-69a9-4877-9df6-c12a9323fa6a.png)


## Step to run our project 

### prerequest
if you are running under wsl2, run this command before clone (optional) 

```
git config --global core.autocrlf false
``` 

if not aws in the local, download aws cli and config aws access id and secret token before make (optional)

```
aws configure
``` 

Get the repo into local.  Update tpl-vars.txt with your own infos and ghio key.

```
git clone https://github.com/scp756-221/term-project-abc.git
cd term-project-abc
cp cluster/tpl-vars-blank.txt cluster/tpl-vars.txt 
echo $github token > cluster/ghcr.io-token.txt

```

### deployment
#### use docker k8s with tool and make template

```
./tools/shell.sh
make -f k8s-tpl.mak templates
```
#### Ensure AWS DynamoDB is accessible/running
```
make -f k8s.mak ls-tables
```

The resulting output should include tables User, Music and Playlist. If not, init a new tables.
```
make -f k8s.mak dynamodb-clean
make -f k8s.mak dynamodb-init
```

#### cluster setup

##### create a cluster

```
make -f eks.mak start
```

##### view cluster

```
kubectl config use-context aws756
```

##### create namespace and switch to it

```
kubectl create ns c756ns
kubectl config set-context aws756 --namespace=c756ns
```

##### Installing the service mesh istio,and inspect in cluster
```
istioctl install -y --set profile=demo --set hub=gcr.io/istio-release
kubectl label namespace c756ns istio-injection=enabled
```

##### build image, make sure they are in public
```
make -f k8s.mak cri
```
##### deploy service
```
make -f k8s.mak gw db s1 s2 s3
```

##### check service(optional)
```
k9s -n c756ns
```



#####  get the external ip address
```
kubectl -n istio-system get service istio-ingressgateway | cut -c -140
```

##### Provisioning the system

```
make -f k8s.mak provision
```

##### load initial data in dynamoDB

```
make -f k8s.mak loader
```





## Monitoring


### Gatling load test
test the service with gatling shell, command needs to run in native environment(not in shell.sh)
gatling - servicename.sh usernumber, for example:

```
./gatling-all.sh 500
```

check gatling runing status

```
docker container list
```

### Grafana
Grafana is a tool that uses for creating and running dashboards. You could see some significant statistics for your current system with Grafana dashboard.

First of all, to get access URL, do: 

```
make -f k8s.mak grafana-url

```
Then, login with 

```
admin
prom-operator
```

### Prometheus
To print the Prometheus URL, run:

```
make -f k8s.mak prometheus-url
```

### Kiali
To get the kiali URL, run:

```
make -f k8s.mak kiali
make -f k8s.mak kiali-url
```

####Set Kiali graph

Namespaces: c756ns
Graph type: Versioned app graph
Display interval: Last 1m
Refresh interval: Every 30s
Display:
Show Edge Labels: Traffic Rate
Show: Compressed Hide, Operation Nodes, Service Nodes, Traffic Animation
Show Badges: Virtual Services

## Finish up
### end the gatling load
```
./tools/kill-gatling.sh
```
### close cluster
```
make -f eks.mak stop
```

## Directory structure

The core of the microservices. `s2/v1.1`, `s2/v2`, and `s2/standalone`  are for use with Assignments. For the term project, the directory works as below
```
├── ./db
├── ./s1
├── ./s2
│   ├── ./s2/standalone
│   │   ├── ./s2/standalone/__pycache__
│   │   └── ./s2/standalone/odd
│   ├── ./s2/test
│   ├── ./s2/v1
│   ├── ./s2/v1.1
│   └── ./s2/v2
│── ./s3
│   │── app.py
│   │── Dockerfile
│   │── README.md
│   │── requirements.txt
```

Other directories: 
- `cluster`: configuration files including github tokens and aws access keys
- `db`: database service
- `gatling`: generate different workload test for the application
- `loader`: for inserting data into the aws DynamoDB table
- `logs`: for storing logs 
- `mcli`: for the music cli
- `s1`: for the user service
- `s2`: for the music service
- `s3`: for the playlist service
- `tools`: bash/python scripts which quickly start docker or aws services


## Troubleshooting

(1) If you see the error below when you try to get URL from Grafana or Prometheus:
```
Error from server (NotFound): namespaces "istio-system" not found
http://:9090/
```
You have to install **istio**
```
istioctl install -y --set profile=demo --set hub=gcr.io/istio-release
```

(2) If you see such errors
```
Error from server (NotFound): services "prom-ingress" not found
Error from server (NotFound): services "grafana-ingress" not found
```
Please provision your system first
```
make -f k8s.mak provision
```
