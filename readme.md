# For test

0. Install minikube (Windows) v1.26.0 and Helm
[doc] https://minikube.sigs.k8s.io/docs/start/

[file] https://github.com/kubernetes/minikube/releases/download/v1.26.0/minikube-windows-amd64.exe

[file] https://get.helm.sh/helm-canary-windows-amd64.zip

1. Start minikube (Windows) v1.26.0

```
minikube start --kubernetes-version=v1.24.2
```

2. Start install script
```
https://raw.githubusercontent.com/YuriyKrasilnikov/k8s-airflow-test/master/script/install.cmd
```

3. View webserver on localhost:80
```
kubectl port-forward svc/webserver 80:8000
```



# For develop and debug (Windows)

You can edit the code locally

1. Install minikube (Windows) v1.26.0 and Helm
[doc] https://minikube.sigs.k8s.io/docs/start/

[file] https://github.com/kubernetes/minikube/releases/download/v1.26.0/minikube-windows-amd64.exe

[file] https://get.helm.sh/helm-canary-windows-amd64.zip

2. git clone https://github.com/YuriyKrasilnikov/k8s-airflow-test.git

3. Start minikube (Windows) v1.26.0
```
minikube start --kubernetes-version=v1.24.2 --mount-string=${PWD}\src:/mnt --mount
```

4. Start install script
```
script\debug\install-debug.cmd
```

5. View webserver on localhost:80
```
kubectl port-forward svc/webserver 80:8000
```