@ECHO OFF
minikube start --kubernetes-version=v1.24.2 --mount-string=$PWD\src:/mnt --mount

helm repo add apache-airflow https://airflow.apache.org

helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace -f .\src\airflow\yaml\override-local.yaml

minikube ssh 'docker build -t file-uploader -f /mnt/golang/.docker/dockerfile /mnt/ --build-arg src="/golang/FileUploader" --no-cache'

kubectl apply -f .\src\k8s\local-models.yaml
kubectl apply -f .\src\k8s\file-uploader.yaml