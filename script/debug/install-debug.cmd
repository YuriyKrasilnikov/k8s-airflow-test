@ECHO OFF

kubectl create namespace airflow

kubectl apply -f .\src\k8s\debug\pvc-dags.yaml
kubectl apply -f .\src\k8s\debug\pvc-models.yaml

helm repo add apache-airflow https://airflow.apache.org

helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace -f .\src\airflow\yaml\debug\override.yaml

minikube ssh "docker build -t file-uploader -f /mnt/golang/.docker/dockerfile /mnt/ --build-arg src='/golang/FileUploader' --no-cache ; docker build -t webserver -f /mnt/python/.docker/dockerfile /mnt/ --build-arg src='/python/WebServer' --no-cache"

kubectl apply -f .\src\k8s\file-uploader.yaml

kubectl apply -f .\src\k8s\webserver.yaml

kubectl apply -f .\src\k8s\ingress.yaml