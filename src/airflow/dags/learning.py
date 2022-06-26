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

args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2022, 6, 25),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}

@task(task_id="learning_fit")
def learning_fit(input_train, output_train, feature_model, output_model, logistic_regression_kargs={}):
    logging.debug('Start learning fit function')

    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import LogisticRegression

    with open(feature_model, 'rb') as f:
      feature_model = pickle.load(f)

    lg = LogisticRegression(**logistic_regression_kargs)

    X_train = pd.read_parquet(input_train) 
    y_train = pd.read_parquet(output_train)

    clf = lg.fit(
      feature_model.transform(X_train),
      y_train
    )

    model = Pipeline([
        ("Feature Engineering", feature_model),
        ("Logistic Regression", clf),
    ])

    with open(output_model, 'wb') as f:
        pickle.dump(model, f)
    
    logging.debug('End learning fit function')


with DAG(dag_id='titanic_learning', default_args=args, schedule_interval=None) as dag:

    learning_fit_task = learning_fit(
      input_train   = INPUT_TRAIN,
      output_train  = OUTPUT_TRAIN,
      feature_model = FEATURE_MODEL,
      output_model = MODEL,
      logistic_regression_kargs={
        "random_state":42
      }
    )
