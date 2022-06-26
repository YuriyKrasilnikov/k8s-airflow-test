import logging
import datetime as dt

from airflow.models import DAG
from airflow.decorators import task

from airflow.providers.http.sensors.http import HttpSensor

AIRFLOW_CONN_HTTP_DEFAULT='http://username:password@servvice.com:80/https?headers=header'

args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2022, 6, 25),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

with DAG(dag_id='connect_test', default_args=args, schedule_interval=None) as dag:
  http_sensor_check_task = HttpSensor(
      task_id='http_sensor_check',
      http_conn_id="",
      endpoint='http://nginx.default.svc.cluster.local',
      method="GET",
      request_params={},
      response_check=lambda response: "httpbin" in response.text,
      poke_interval=5,
      dag=dag,
  )