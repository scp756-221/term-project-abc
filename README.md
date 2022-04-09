[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7281378&assignment_repo_type=AssignmentRepo)

# SFU CMPT756 Term Project 
This is the repo maintained by team-abc for the CMPT756 final project

Our primary goal is to implement a playlist microservice in addition to S1 (user) and S2 (music) services. It contains a new database table and a series of the corresponding APIs to manipulate data. Please see the architecture for our microservices below. 

![mircroservice achitecture](https://user-images.githubusercontent.com/39822436/162517769-de65a5f9-69a9-4877-9df6-c12a9323fa6a.png)

Done: 

1. Finish the implementation of the S3 (playlist) microservice.
2. Build and deploy all microservices on Kubernetes clusters. 

Todo: 

1. Grafana testing. 
2. Galting to do performance testing 
3. Potentially a recommendation system to suggest music to users 

## Step to run our project 

1. Get the repo into local
```
git clone https://github.com/scp756-221/term-project-abc.git
cd term-project-abc
./tools/shell.sh
```
(optional)for running under wsl2, run this command before clone 
```
git config --global core.autocrlf false
``` 

2. update tpl-vars.txt with your own infos
```
cp cluster/tpl-vars-blank.txt cluster/tpl-vars.txt 
echo $github token > cluster/ghcr.io-token.txt
make -f k8s-tpl.mak templates
make -f allclouds.mak
```
(optional)if not aws in the local, download aws cli and config aws access id and secret token before make 
```
aws configure
``` 

3. Try out these instructions in assignment 4
```
make -f eks.mak start
kubectl config use-context aws756
kubectl create ns c756ns
kubectl config set-context aws756 --namespace=c756ns
kubectl config use-context aws756
istioctl install -y --set profile=demo --set hub=gcr.io/istio-release
kubectl label namespace c756ns istio-injection=enabled
kubectl get svc --all-namespaces | cut -c -140
```

4. Build & push the images up to the CR. Check if there's the image of s3 in your Github package after calling this command and change the visibility to public
```
make -f k8s.mak cri
make -f k8s.mak gw db s1 s2 s3
```

5. start k9s to check if the services are deployment successfully k9s


