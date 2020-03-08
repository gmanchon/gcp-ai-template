import numpy as np
import pandas as pd

from google.cloud import storage

from sklearn.externals import joblib

from sklearn.linear_model import LinearRegression

from Model.conf import *

def get_data():
    '''retrieve train data from bucket'''
    client = storage.Client()
    df = pd.read_csv("gs://{}/{}".format(
            BUCKET_NAME,
            BUCKET_DATA_TRAIN_PATH),
        nrows=1_000)
    return df

def preprocess(df):
    '''process X and y from data and preprocess data'''
    X_train = df[['Agencia_ID']]
    y_train = df['Demanda_uni_equil']
    return X_train, y_train

def train_model(X_train, y_train):
    '''train model'''
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    print('model trained')
    return lr

def save_model(model):
    '''dump model and upload to gcp'''
    local_model_name = BUCKET_MODEL_DUMP_NAME
    joblib.dump(model, local_model_name)

    client = storage.Client().bucket(BUCKET_NAME)
    storage_location = '{}/{}/{}/{}'.format(
        BUCKET_MODEL_PATH,
        BUCKET_MODEL_NAME,
        BUCKET_MODEL_VERSION,
        local_model_name)
    blob = client.blob(storage_location)
    blob.upload_from_filename(local_model_name)
    print('model uploaded')

# retrieve data
df = get_data()

# get X and y
X_train, y_train = preprocess(df)

# retrieve model
model = train_model(X_train, y_train)

# dump model and upload to gcp
save_model(model)
