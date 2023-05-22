# dataflow-python-ci-cd

The Medium article for this use case :

https://medium.com/@mazlum.tosun/ci-cd-for-dataflow-java-with-flex-templates-and-cloud-build-e3c584b8e564

## Run job with Dataflow runner from local machine :

```bash
python -m team_league.application.team_league_app \
    --project=gb-poc-373711 \
    --project_id=gb-poc-373711 \
    --input_json_file=gs://mazlum_dev/team_league/input/json/input_teams_stats_raw.json \
    --job_name=team-league-python-job-$(date +'%Y-%m-%d-%H-%M-%S') \
    --runner=DataflowRunner \
    --staging_location=gs://mazlum_dev/dataflow/staging \
    --region=europe-west1 \
    --setup_file=./setup.py \
    --temp_location=gs://mazlum_dev/dataflow/temp \
    --team_league_dataset="mazlum_test" \
    --team_stats_table="team_stat"
```

## Build image with Cloud Build :

```bash
gcloud builds submit --tag europe-west1-docker.pkg.dev/gb-poc-373711/internal-images/dataflow/team-league-python:latest .
```

## Create Flex Template spec file :

```bash
gcloud dataflow flex-template build gs://mazlum_dev/dataflow/templates/team_league/python/team-league-python.json \
  --image-gcr-path "europe-west1-docker.pkg.dev/gb-poc-373711/internal-images/dataflow/team-league-python:latest" \
  --sdk-language "PYTHON" \
  --flex-template-base-image "PYTHON3" \
  --metadata-file "config/metadata.json" \
  --py-path "." \
  --env "FLEX_TEMPLATE_PYTHON_PY_FILE=team_league/application/team_league_app.py" \
  --env "FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE=team_league/requirements.txt" \
  --env "FLEX_TEMPLATE_PYTHON_SETUP_FILE=setup.py"
```

# Run a Flex Template pipeline :

```bash
gcloud dataflow flex-template run "team-league-python-`date +%Y%m%d-%H%M%S`" \
    --template-file-gcs-location "gs://mazlum_dev/dataflow/templates/team_league/python/team-league-python.json" \
    --project=gb-poc-373711 \
    --region=europe-west1 \
    --temp-location=gs://mazlum_dev/dataflow/temp \
    --staging-location=gs://mazlum_dev/dataflow/staging \
    --parameters service_account_email=sa-dataflow-dev@gb-poc-373711.iam.gserviceaccount.com \
    --parameters input_json_file=gs://mazlum_dev/team_league/input/json/input_teams_stats_raw.json \
    --parameters team_league_dataset=mazlum_test \
    --parameters team_stats_table=team_stat
```

# Deploy and run the template with Cloud Build from local machine

### Set env vars in your Shell

```shell
export PROJECT_ID={{your_project_id}}
export LOCATION={{your_location}}
```

### Deploy the Dataflow job with Cloud Build

```shell
gcloud builds submit \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --config dataflow-deploy-job.yaml \
    --substitutions _REPO_NAME="internal-images",_IMAGE_NAME="dataflow/team-league-python",_IMAGE_TAG="latest",_METADATA_TEMPLATE_FILE_PATH="gs://mazlum_dev/dataflow/templates/team_league/python/team-league-python.json",_SDK_LANGUAGE="PYTHON",_PY_PATH=".",_FLEX_TEMPLATE_BASE_IMAGE="PYTHON3",_METADATA_FILE="config/metadata.json",_FLEX_TEMPLATE_PYTHON_PY_FILE="team_league/application/team_league_app.py",_FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="team_league/requirements.txt" \
    --verbosity="debug" .
```

### Run the Dataflow job with Cloud Build

```shell
gcloud builds submit \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --config dataflow-run-job.yaml \
    --substitutions _JOB_NAME="team-league-python",_METADATA_TEMPLATE_FILE_PATH="gs://mazlum_dev/dataflow/templates/team_league/python/team-league-python.json",_TEMP_LOCATION="gs://mazlum_dev/dataflow/temp",_STAGING_LOCATION="gs://mazlum_dev/dataflow/staging",_SA_EMAIL="sa-dataflow-dev@gb-poc-373711.iam.gserviceaccount.com",_INPUT_FILE="gs://mazlum_dev/team_league/input/json/input_teams_stats_raw.json",_SIDE_INPUT_FILE="gs://mazlum_dev/team_league/input/json/input_team_slogans.json",_TEAM_LEAGUE_DATASET="mazlum_test",_TEAM_STATS_TABLE="team_stat" \
    --verbosity="debug" .
```

# Deploy and run the template with Cloud Build with triggers

### Run unit tests with automatic trigger on Github repository

```bash
gcloud beta builds triggers create github \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --repo-name=dataflow-python-ci-cd \
    --repo-owner=tosun-si \
    --branch-pattern=".*" \
    --build-config=dataflow-run-tests.yaml \
    --include-logs-with-status \
    --verbosity="debug"
```

### Deploy the Flex Template with a manual trigger on Github repository

```bash
gcloud beta builds triggers create manual \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --name="deploy-dataflow-template-team-league-python" \
    --repo="https://github.com/tosun-si/dataflow-python-ci-cd" \
    --repo-type="GITHUB" \
    --branch="main" \
    --build-config="dataflow-deploy-job.yaml" \
    --substitutions _REPO_NAME="internal-images",_IMAGE_NAME="dataflow/team-league-python",_IMAGE_TAG="latest",_METADATA_TEMPLATE_FILE_PATH="gs://mazlum_dev/dataflow/templates/team_league/python/team-league-python.json",_SDK_LANGUAGE="PYTHON",_FLEX_TEMPLATE_BASE_IMAGE="PYTHON3",_PY_PATH=".",_FLEX_TEMPLATE_PYTHON_PY_FILE="team_league/application/team_league_app.py",_FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="team_league/requirements.txt" \
    --verbosity="debug"
```

### Run the Flex Template with a manual trigger on Github repository

```bash
gcloud beta builds triggers create manual \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --name="run-dataflow-template-team-league-python" \
    --repo="https://github.com/tosun-si/dataflow-python-ci-cd" \
    --repo-type="GITHUB" \
    --branch="main" \
    --build-config="dataflow-run-job.yaml" \
    --substitutions _JOB_NAME="team-league-python",_METADATA_TEMPLATE_FILE_PATH="gs://mazlum_dev/dataflow/templates/team_league/python/team-league-python.json",_TEMP_LOCATION="gs://mazlum_dev/dataflow/temp",_STAGING_LOCATION="gs://mazlum_dev/dataflow/staging",_SA_EMAIL="sa-dataflow-dev@gb-poc-373711.iam.gserviceaccount.com",_INPUT_FILE="gs://mazlum_dev/team_league/input/json/input_teams_stats_raw.json",_TEAM_LEAGUE_DATASET="mazlum_test",_TEAM_STATS_TABLE="team_stat" \
    --verbosity="debug"
```
