import logging
import datetime as dt

import pickle

import pandas as pd

from airflow.models import DAG
from airflow.decorators import task

### install packages ###
from utils import *
packages_installed(["sklearn"])

### import settings ###
from settings import *

### import predict ###
from settings import *

args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2022, 6, 25),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

### Task ###
@task(task_id="classification_report")
def test(input_model, input_test, output_test):
    logging.debug('Start predict and classification report function')

    from sklearn.metrics import classification_report

    X_test = pd.read_parquet(input_test)
    y_test = pd.read_parquet(output_test)

    with open(input_model, 'rb') as f:
      model = pickle.load(f)

    y_pred = model.predict(X_test)

    logging.info(
        "\n"+classification_report(y_test, y_pred)
    )

    logging.debug('End predict and classification report function')


### Dags ###
with DAG(dag_id='titanic_predict_test', default_args=args, schedule_interval=None) as dag:
    test_task = test(
        input_model = MODEL,
        input_test  = INPUT_TEST,
        output_test = OUTPUT_TEST
    )