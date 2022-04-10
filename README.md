[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7281378&assignment_repo_type=AssignmentRepo)

# SFU CMPT756 Term Project 
This is the repo maintained by team-abc for the CMPT756 final project

Our primary goal is to implement a playlist microservice in addition to S1 (user) and S2 (music) services. It contains a new database table and a series of the corresponding APIs to manipulate data. Please see the architecture for our microservices below. 

![mircroservice achitecture](https://user-images.githubusercontent.com/39822436/162517769-de65a5f9-69a9-4877-9df6-c12a9323fa6a.png)


## Step to run our project 

   if you are running under wsl2, run this command before clone (optional) 
```
git config --global core.autocrlf false
``` 

1. Get the repo into local
```
git clone https://github.com/scp756-221/term-project-abc.git
cd term-project-abc
./tools/shell.sh
```

if not aws in the local, download aws cli and config aws access id and secret token before make (optional)
```
aws configure
``` 

2. Update tpl-vars.txt with your own infos  

**this step is important, you need to create aws access keys and github signon tokens accordingly**
```
cp cluster/tpl-vars-blank.txt cluster/tpl-vars.txt 
echo $github token > cluster/ghcr.io-token.txt
make -f k8s-tpl.mak templates
make -f allclouds.mak
```

3. cluster setup instructions (quote from assignment 4)
```
make -f eks.mak start
kubectl config use-context aws756
kubectl create ns c756ns
kubectl config set-context aws756 --namespace=c756ns
istioctl install -y --set profile=demo --set hub=gcr.io/istio-release
kubectl label namespace c756ns istio-injection=enabled
kubectl get svc --all-namespaces | cut -c -140
```

4. Build & push the docker images. Go to github package page https://github.com/USERNAME?tab=packages, change the visibility of s3 to public if first time runningthe visibility to public
```
make -f k8s.mak cri
make -f k8s.mak gw db s1 s2 s3
```

5. Start k9s to check if the services are deployment successfully k9s


## Monitoring

### Provisioning the system

if you do not have a cluster running, please do:
```
make -f eks.mak start
```
otherwise, directly run: 
```
make -f k8s.mak provision
```

### Grafana
Grafana is a tool that uses for creating and running dashboards. You could see some significant statistics for your current system with Grafana dashboard.

First of all, to get access URL, do: 
```
$ make -f k8s.mak grafana-url
http://a3a64fbacc7114a028faa18b4a710f87-1707422240.us-west-2.elb.amazonaws.com:3000/
```
Then, login with 
```
admin
prom-operator
```
### load dynamoDB
```
make -f k8s.mak loader
```
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
