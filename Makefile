# do not use inline comments at the end of the lines,
# they add additional spaces in the content of the variables,
# which generates errors

#   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-
#  / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \
# `-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'
#
# variables extraction
#

# conf file
CONF_FILE=Model/conf.py

# extract variables
PACKAGE_NAME=$(shell    grep "^PACKAGE_NAME="    ${CONF_FILE} | cut -d"=" -f2)
FILENAME=$(shell        grep "^FILENAME="        ${CONF_FILE} | cut -d"=" -f2)
PRED_FILENAME=$(shell   grep "^PRED_FILENAME="   ${CONF_FILE} | cut -d"=" -f2)
PROJECT_ID=$(shell      grep "^PROJECT_ID="      ${CONF_FILE} | cut -d"=" -f2)
REGION=$(shell          grep "^REGION="          ${CONF_FILE} | cut -d"=" -f2)
PYTHON_VERSION=$(shell  grep "^PYTHON_VERSION="  ${CONF_FILE} | cut -d"=" -f2)
RUNTIME_VERSION=$(shell grep "^RUNTIME_VERSION=" ${CONF_FILE} | cut -d"=" -f2)
FRAMEWORK=$(shell       grep "^FRAMEWORK="       ${CONF_FILE} | cut -d"=" -f2)
BUCKET_NAME=$(shell     grep "^BUCKET_NAME="     ${CONF_FILE} | cut -d"=" -f2)
JOB_FOLDER=$(shell      grep "^JOB_FOLDER="      ${CONF_FILE} | cut -d"=" -f2)
JOB_PREFIX=$(shell      grep "^JOB_PREFIX="      ${CONF_FILE} | cut -d"=" -f2)

# tmp variables
JOB_NAME=${JOB_PREFIX}_$(shell date +'%Y%m%d_%H%M%S')

# manual extract
REQUIREMENTS=$(shell awk '/REQUIRED_PACKAGES=\[/,/]/' ${CONF_FILE})

variables:
	@echo package name: ${PACKAGE_NAME}
	@echo filename: ${FILENAME}
	@echo pred filename: ${PRED_FILENAME}
	@echo project id: ${PROJECT_ID}
	@echo region: ${REGION}
	@echo python version: ${PYTHON_VERSION}
	@echo runtime version: ${RUNTIME_VERSION}
	@echo framework: ${FRAMEWORK}
	@echo bucket name: ${BUCKET_NAME}
	@echo job folder: ${JOB_FOLDER}
	@echo job prefix: ${JOB_PREFIX}
	@echo job name: ${JOB_NAME}
	@echo requirements: ${REQUIREMENTS}

# ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^ ~ ^
#
# ai tasks
#

# auth to gcp
auth:
	-@gcloud auth login

# define project id
set_project:
	-@gcloud config set project ${PROJECT_ID}

# installs locally required packages
pip_install_reqs:
	python req.py "${REQUIREMENTS}"

# train model locally
run_locally:
	@python -m ${PACKAGE_NAME}.${FILENAME}

# train model on gcp
gcp_submit_training:
	gcloud ai-platform jobs submit training ${JOB_NAME} \
		--job-dir "gs://${BUCKET_NAME}/${JOB_FOLDER}" \
		--package-path ${PACKAGE_NAME} \
		--module-name ${PACKAGE_NAME}.${FILENAME} \
		--region ${REGION} \
		--python-version=${PYTHON_VERSION} \
		--runtime-version=${RUNTIME_VERSION} \
		--stream-logs

# ask gcp for pred
pred_from_gcp:
	@python -m ${PACKAGE_NAME}.${PRED_FILENAME}
