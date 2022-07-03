@ECHO OFF

minikube ssh "sudo apt-get update ; sudo apt-get install git -y ; git clone https://github.com/YuriyKrasilnikov/k8s-airflow-test.git /home/docker/k8s-airflow-test"

kubectl apply -f https://raw.githubusercontent.com/YuriyKrasilnikov/k8s-airflow-test/master/src/k8s/pvc-models.yaml

helm repo add apache-airflow https://airflow.apache.org

helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace -f https://raw.githubusercontent.com/YuriyKrasilnikov/k8s-airflow-test/master/src/airflow/yaml/override.yaml

minikube ssh "docker build -t file-uploader -f /home/docker/k8s-airflow-test/src/golang/.docker/dockerfile /home/docker/k8s-airflow-test/src/ --build-arg src='/golang/FileUploader' --no-cache"
minikube ssh "docker build -t webserver -f /home/docker/k8s-airflow-test/src/python/.docker/dockerfile /home/docker/k8s-airflow-test/src/ --build-arg src='/python/WebServer' --no-cache"

kubectl apply -f https://raw.githubusercontent.com/YuriyKrasilnikov/k8s-airflow-test/master/src/k8s/file-uploader.yaml

kubectl apply -f https://raw.githubusercontent.com/YuriyKrasilnikov/k8s-airflow-test/master/src/k8s/webserver.yaml