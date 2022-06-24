# For test

1. Start minikube (Windows) v1.26.0

```
minikube start --kubernetes-version=v1.24.2
```

2. Airflow. Installing the Chart 

```
helm repo add apache-airflow https://airflow.apache.org

helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace -f .\src\airflow\yaml\override-git.yaml

```

Airflow Webserver:

```
kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow
```


# For develop

You can edit the code locally

1. Start minikube (Windows) v1.26.0

```
minikube start --kubernetes-version=v1.24.2 --mount-string=$PWD\src:/mnt --mount
```

2. Airflow. Installing the Chart 

```
helm repo add apache-airflow https://airflow.apache.org

helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace -f .\src\airflow\yaml\override-local.yaml
```

```
kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow
```

Default Webserver (Airflow UI) Login credentials:

    username: admin
    password: admin

Default Postgres connection credentials:

    username: postgres
    password: postgres
    port:     5432