
from cmath import e
from fastapi import FastAPI, Depends, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import pickle
import pandas as pd

import requests
import json

from settings import *

app = FastAPI()

class Passenger(BaseModel):
    pclass: int
    name: str | None = None
    sex: str
    age: float
    ssaboard: int
    pcaboard: int
    fare: float
    
    @classmethod
    def as_form(cls,
      pclass: int = Form(...),
      name: str = Form(...),
      sex: str = Form(...),
      age: float = Form(...),
      ssaboard: int = Form(...),
      pcaboard: int = Form(...),
      fare: float = Form(...)
    ):
        return cls(
          pclass=pclass,
          name=name,
          sex=sex,
          age=age,
          ssaboard=ssaboard,
          pcaboard=pcaboard,
          fare=fare
          )

class ResultArray(BaseModel):
  result: list[int] | None = None

@app.post("/retrain")
def retrain():
  rq = requests.post(
    AIRFLOW_API_HOST,
    headers=AIRFLOW_HEADERS, 
    auth=AIRFLOW_AUTH, 
    data=json.dumps(AIRFLOW_BODY)
  )

  return rq.content


@app.post("/predict")
def predict(request: Passenger  = Depends(Passenger.as_form)):

    try:
      with open(MODEL, 'rb') as f:
        model = pickle.load(f)
    except:
      return {
        "Error": "Need create model"
      }

    result = model.predict(
      pd.DataFrame(
        [
          request.dict().values()
        ],
        columns=COLUMNS
      )
    )

    return {
      "Result": result.tolist()
    }

app.mount(
  "/",
  StaticFiles(directory="static", html = True),
  name="static"
)
