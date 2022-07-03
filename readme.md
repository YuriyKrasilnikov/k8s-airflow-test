# For test

1. Start minikube (Windows) v1.26.0

```
minikube start --kubernetes-version=v1.24.2
```



# For develop and debug (Windows)

You can edit the code locally

0. Install minikube (Windows) v1.26.0
[doc] https://minikube.sigs.k8s.io/docs/start/
[file] https://github.com/kubernetes/minikube/releases/download/v1.26.0/minikube-windows-amd64.exe

1. Start minikube (Windows) v1.26.0
```
minikube start --kubernetes-version=v1.24.2 --mount-string=${PWD}\src:/mnt --mount
```

2. Start install script
```
script\debug\install-debug.cmd
```

3. View webserver on localhost:80
```
kubectl port-forward svc/webserver 80:8000
```