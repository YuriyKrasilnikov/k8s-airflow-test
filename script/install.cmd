@ECHO OFF

minikube ssh "sudo apt-get update ; sudo apt-get install git -y ; cd /mnt ; git clone https://github.com/YuriyKrasilnikov/k8s-airflow-test.git"