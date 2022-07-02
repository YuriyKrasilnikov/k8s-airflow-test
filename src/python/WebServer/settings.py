
import os

### Consts ###

PATHNAME = 'data'
MODEL_FILENAME = 'model.pickle'

PATH = os.path.join(
  os.getenv('APP_PATH'),
  PATHNAME
)

if not os.path.exists(PATH):
    os.makedirs(PATH)

def _add_path(filename):
  return os.path.join(PATH, filename)

MODEL = _add_path(MODEL_FILENAME)

COLUMNS = ["Pclass", "Name", "Sex", "Age", "Siblings/Spouses Aboard", "Parents/Children Aboard", "Fare"]


AIRFLOW_HOST = "http://"+os.getenv('AIRFLOW_HOST')

AIRFLOW_RUNDAGS = "titanic"

AIRFLOW_API_PATH = "/api/v1/dags/"+AIRFLOW_RUNDAGS+"/dagRuns"

AIRFLOW_API_HOST = AIRFLOW_HOST+AIRFLOW_API_PATH

AIRFLOW_HEADERS = {
  'accept': 'application/json',
  'Content-Type': 'application/json',
}

AIRFLOW_AUTH = ('admin', 'admin')

AIRFLOW_BODY = {
  "conf": {}
}


