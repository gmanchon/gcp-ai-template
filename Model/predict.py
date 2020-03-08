import numpy as np
import pandas as pd

from google.cloud import storage

import googleapiclient.discovery

from Model.conf import *

def get_test_data():
    '''retrieve test data from bucket'''
    client = storage.Client()
    df = pd.read_csv("gs://{}/{}".format(
            BUCKET_NAME,
            BUCKET_DATA_TEST_PATH),
        nrows=1_000)
    return df

def preprocess(df):
    '''process X and y from data and preprocess data'''
    '''preprocess should be identical to the one used on train data'''
    X_test = df[['Agencia_ID']]
    y_test = None
    return X_test, y_test

def convert_to_json_instances(X_test):
    return X_test.values.tolist()

def predict_json(project, model, instances, version=None):
    '''call model for prediction'''
    # do not change the ml and v1 parameters, they correspond to the gcp ml api
    service = googleapiclient.discovery.build('ml', 'v1') # google api endpoint /ml/v1
    name = 'projects/{}/models/{}'.format(project, model)
    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()
    if 'error' in response:
        raise RuntimeError(response['error'])
    return response['predictions']

# get data
df = get_test_data().head(100) # only predict for the first 100 rows

# apply preprocessing
X_test, y_test = preprocess(df)

# convert X_test to json
instances = convert_to_json_instances(X_test)

# send request and get response
results = predict_json(project=PROJECT_ID,
    model=BUCKET_MODEL_NAME,
    version=BUCKET_MODEL_VERSION,
    instances=instances)

print(results)
