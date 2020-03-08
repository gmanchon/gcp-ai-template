#   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
#  / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
# `-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
#
# this file is used by Makefile for various tasks
# and by setup.py for gcp setup
# and by model train code
# and by model predict code
#

# ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^
#
# python model package
#

# folder name
PACKAGE_NAME="Model"
PACKAGE_DESCRIPTION="static prediction model"

# file name
FILENAME="trainer"
PRED_FILENAME="predict"

# ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^
#
# gcp project
#

# project id
PROJECT_ID="le-wagon-data-grupo-bimbo"

# ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^
#
# gcp ai platform
#

# model training conf
REGION="europe-west1"
PYTHON_VERSION=3.7
RUNTIME_VERSION=1.15
FRAMEWORK="scikit-learn"

REQUIRED_PACKAGES=[
    'google-cloud-storage==1.26.0',
    'gcsfs==0.6.0',
    'pandas==0.24.2',
    'scipy==1.2.2',
    'scikit-learn==0.20.4']

# ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^
#
# gcp storage
#

# model training bucket
BUCKET_NAME="wagon-data-grupo-bimbo-sales"

# data folder
BUCKET_DATA_PATH='data'                           # data folder
BUCKET_DATA_TRAIN_PATH='data/train_100k.csv'      # train csv path
BUCKET_DATA_TEST_PATH='data/test_10k.csv'         # test csv path

# models folder
BUCKET_MODEL_PATH='models'                        # models folder
BUCKET_MODEL_NAME='static_baseline_fixed_resp_4'  # model name
BUCKET_MODEL_VERSION='v_1'                        # will store model.joblib
BUCKET_MODEL_DUMP_NAME='model.joblib'             # required dump name (do not change this)

# model training folder
JOB_FOLDER="trainings"

# job prefix
JOB_PREFIX="static_model"
