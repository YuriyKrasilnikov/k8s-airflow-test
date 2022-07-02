
import os

### Consts ###

URL = 'https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv'

PATHNAME = 'data'
FILENAME = 'data.csv'

INPUT_TRAIN_FILENAME  = "input_train.parquet"
INPUT_TEST_FILENAME   = "input_test.parquet"
OUTPUT_TRAIN_FILENAME = "output_train.parquet"
OUTPUT_TEST_FILENAME  = "output_test.parquet"

FEATURE_MODEL_FILENAME = 'feature_model.pickle'
MODEL_FILENAME = 'model.pickle'

PATH = os.path.join(os.path.expanduser('~'), PATHNAME)
if not os.path.exists(PATH):
    os.makedirs(PATH)

def _add_path(filename):
  return os.path.join(PATH, filename)

FILE = _add_path(FILENAME)

INPUT_TRAIN = _add_path(INPUT_TRAIN_FILENAME)
INPUT_TEST = _add_path(INPUT_TEST_FILENAME)
OUTPUT_TRAIN = _add_path(OUTPUT_TRAIN_FILENAME)
OUTPUT_TEST = _add_path(OUTPUT_TEST_FILENAME)

FEATURE_MODEL = _add_path(FEATURE_MODEL_FILENAME)
MODEL = _add_path(MODEL_FILENAME)

DROP_COLUMNS = ["Name"]
CATEGORATE_COLUMNS = ["Sex"]

FILE_CONN_HTTP = 'http://file-uploader.default.svc.cluster.local:8080/upload'
