import logging
import datetime as dt

import requests
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

### Task ###

@task(task_id="download_dataset")
def download_dataset(url, output_file):
    logging.debug('Start download dataset function')

    logging.debug('Start requests url: '+url)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    logging.debug('Start save data to filename: '+output_file)
    with open(output_file, 'w', encoding='utf-8') as f:
        for chunk in response.iter_lines():
            f.write('{}\n'.format(chunk.decode('utf-8')))
    logging.debug('End download dataset function')


@task(task_id="split_dataset")
def split_dataset(file, input_train, input_test, output_train, output_test):
    logging.debug('Start split dataset function')

    from sklearn.model_selection import train_test_split

    data = pd.read_csv(file)

    X_train, X_test, y_train, y_test = train_test_split(data.drop("Survived", axis=1), data["Survived"], test_size=0.33, random_state=42)
    X_train.to_parquet(input_train)
    X_test.to_parquet(input_test)
    y_train.to_frame().to_parquet(output_train)
    y_test.to_frame().to_parquet(output_test)
    logging.debug('End split dataset function')

@task(task_id="feature_engineering_fit")
def feature_engineering_fit(input_train, output_model, catg_colunms, drop_columns=[]):
    logging.debug('Start feature engineering fit function')

    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    train=pd.read_parquet(input_train)

    cols_tr = ColumnTransformer(
        transformers = [
            ("Drop", "drop", drop_columns),
            ("OneHotEncoder", OneHotEncoder(), catg_colunms)
        ],
        remainder='passthrough'
    )

    pipeline = Pipeline([
        ("Drop", cols_tr),
        ("SimpleImputer", SimpleImputer(strategy='mean')),
        ("StandardScaler", StandardScaler(with_mean=False))
    ])

    model = pipeline.fit(train)

    with open(output_model, 'wb') as f:
        pickle.dump(model, f)
    
    logging.debug('End feature engineering fit function')

    

### Dags ###

with DAG(dag_id='titanic_feature_engineering', default_args=args, schedule_interval=None) as dag:

    create_titanic_task = download_dataset(
        url=URL,
        output_file=FILE
    )

    split_titanic_task = split_dataset(
        file            = FILE,
        input_train     = INPUT_TRAIN,
        input_test      = INPUT_TEST,
        output_train    = OUTPUT_TRAIN,
        output_test     = OUTPUT_TEST
    )

    feature_engineering_fit_task = feature_engineering_fit(
        input_train=INPUT_TRAIN,
        output_model=FEATURE_MODEL,
        catg_colunms=CATEGORATE_COLUMNS,
        drop_columns= DROP_COLUMNS
    )

    create_titanic_task >> split_titanic_task >> feature_engineering_fit_task