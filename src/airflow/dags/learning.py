import logging
import datetime as dt

import pickle

import pandas as pd

import requests

from airflow.utils.task_group import TaskGroup
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

@task(task_id="upload_file")
def upload_file(url, model):
    logging.debug('Start upload file function')

    with open(model, 'rb') as f:
        response = requests.post(
            url,
            files={
                "file": f
            }
        )
        logging.debug(f"status code {response.status_code}")
        logging.debug(f"body {response.content}")


    logging.debug('End upload file function')


def learning_model(name, task_arg):
    group = TaskGroup(
        group_id=name,
    )

    with group:

      learning_fit_task = learning_fit(
        input_train   = task_arg.INPUT_TRAIN,
        output_train  = task_arg.OUTPUT_TRAIN,
        feature_model = task_arg.FEATURE_MODEL,
        output_model  = task_arg.MODEL,
        logistic_regression_kargs={
          "random_state":42
        }
      )

      upload_file_task = upload_file(
          url   = task_arg.FILE_CONN_HTTP,
          model = task_arg.MODEL
      )

      learning_fit_task >> upload_file_task

    return group
