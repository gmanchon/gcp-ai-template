
# sources

[gcp day 5 correction](https://github.com/lewagon/taxi-fare) contains a working solution with a different file architecture

[gcp day 4 notebook instructions](https://github.com/lewagon/data-challenges/blob/master/05-Production/04-Deploy-to-Production/Challenge/04-Deploy-to-Production-Challenge.ipynb) contains informations required in order to setup the gcp account

# usage

1. conf: fill all the variables in `Model/conf.py`
2. train: fill `Model/trainer.py` with the code used in order to train your model
3. predict: fill `Model/predict.py` with the code used in order to predict with your trained model
4. if you feel the need to change the name of the `Model` package, please update:
- `CONF_FILE` in `Makefile`
- `from Model.conf` in `setup.py`, `trainer.py` and `predict.py`
- `PACKAGE_NAME` in `conf.py`
- and rename the `Model` folder

# how does this work?

## gcp setup

you will find instructions below

## package

`Makefile` allows you to launch several tasks (listed below) in order to setup your local environment, train locally or on gcp, and make a prediction using a trained model on gcp

`req.py` is used by the `pip_install_reqs` task in order to extract `REQUIRED_PACKAGES` from `Model/conf.py` (using a single file limits the risk that the environment is not the same locally and on gcp)

`setup.py` is used by gcp in order to setup the training environement

## model

`conf.py` stores the variables of the project (package name and entry file, gcp project, model, model version, bucket)

`predict.py` can be used outside of the package and is used locally in order to request from gcp a prediction by a trained model

`trainer.py` is required to be provided inside of the package in order to train on gcp

## ruby predition

`Gemfile` contains the gems required for interaction with gcp storage (buckets) and ai platform (prediction)

do not forget that every time you ommit to `bundle install` after editing a `Gemfile`, a TA dies somewhere

`sales_controller.rb` contains everything you need in order to make a prediction from a trained model in gcp

# tasks

## show project conf

``` zsh
make                                    # lists all project variables
make variables                          # lists all project variables
```

## install local requirements

``` zsh
make pip_install_reqs                   # installs locally all requirements
```

## train locally

``` zsh
python Model/trainer.py                 # trains model locally
python -m Model.trainer                 # trains model locally
make run_locally                        # trains model locally
```

## train on gcp

``` zsh
make auth                               # logins to gcp
make set_project                        # sets gcp project
make gcp_submit_training                # trains model on gcp
```

## predict locally

``` zsh
python Model/predict.py                 # asks gcp for a prediction
python -m Model.predict                 # asks gcp for a prediction
make pred_from_gcp                      # asks gcp for a prediction
```

# gcp setup

[gcp console](https://console.cloud.google.com/home/)

[runtime versions](https://cloud.google.com/ai-platform/training/docs/runtime-version-list)

gcp services:
- api & services: handles credentials, service accounts, and keys
- storage: handles buckets
- ai platform: handles models, model versions, and jobs

## setup gcp for model training and prediction

### create a project

connect to the [gcp console](https://console.cloud.google.com/)
in the menu bar, select or create a `new project`
- fill `project name`: Le Wagon Data Grupo Bimbo

### create a bucket to store data, trained models and training data

in `navigation menu`, `storage`, `create bucket`
- bucket name: wagon-data-grupo-bimbo-sales
- `location type`: region
- `location`: europe-west-1 (Belgium)
- `default storage class`: Standard
- `access control`: Fine-grained
- `encryption`: Google-managed key

create folders
- `data` to store csv files
- `models` to store the models and their versions
- models / `static_baseline_fixed_resp_4` for first model
- models / static_baseline_fixed_resp_4 / `v_1` for first model version
- `trainings` to store training tmp data

upload csv files (train, test, etc) to `data` folder

### enable api for project

[enable api](https://console.cloud.google.com/flows/enableapi?apiid=ml.googleapis.com,compute_component&_ga=2.269215094.662509797.1580849510-2071889129.1567861089&_gac=1.154971594.1580849512.CjwKCAiAyeTxBRBvEiwAuM8dnbZ6uMwizbZW44J2mBCX6ncEjwjwpgF8S8QsvhYAXLkJ8awDnIRTNRoCJ_0QAvD_BwE)

### create api credentials json key

in `navigation menu`, `api & services`, `credentials`, `create credentials`, `service account`
- `service account name`: random service account
- `service account id`: random-service-account
- create
- `role`: project / owner
- create key
- `key type`: json

or [use this link](https://console.cloud.google.com/apis/credentials/serviceaccountkey)

store on disk and edit `~/.zshrc` to add env variable

``` zsh
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
```

``` zsh
echo $GOOGLE_APPLICATION_CREDENTIALS
cat $(echo $GOOGLE_APPLICATION_CREDENTIALS)
```

### create a model version for existing model.joblib

#### copy model to bucket

in `navigation menu`, `storage`, wagon-data-grupo-bimbo-sales, in
- wagon-data-grupo-bimbo-sales
- models
- static_baseline_fixed_resp_4
- v_1
- `upload files` model.joblib

#### create model version

[available runtimes](https://cloud.google.com/ai-platform/training/docs/runtime-version-list
)

in `navigation menu`, `ai platform`, `models`, `create bucket`

enable `AI Platform Training & Prediction API`

create model
- `model name`: static_baseline_fixed_resp_4
- `region`: europe-west-1

select model, `create a version`
- `name`: v_1
- `python version`: 3.7
- `framework`: scikit-learn
- `framework version`: 0.20.4
- `ml runtime version`: 1.15
- `machine type`: ai platform machine types / single core cpu
- model uri: browse / wagon-data-grupo-bimbo-sales / models / static_baseline_fixed_resp_4 / v_1 / select (generates wagon-data-grupo-bimbo-sales/models/static_baseline_fixed_resp_4/v_1/)
- save
