import datetime as dt

from airflow import DAG

### import settings ###
from feature_engineering import feature_engineering
from learning import learning_model

### import settings ###
import settings

args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2022, 6, 25),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

with DAG(
    dag_id="titanic",
    default_args=args,
    schedule_interval=None
) as dag:

    feature_engineering_task = feature_engineering(
        name        = "feature_engineering",
        task_arg    = settings,
    )

    learning_model_task = learning_model(
        name        = "learning_model",
        task_arg    = settings,
    )

    feature_engineering_task >> learning_model_task
    
