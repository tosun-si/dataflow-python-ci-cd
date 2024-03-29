# dataflow-python-ci-cd

The Medium article for this use case :

https://medium.com/@mazlum.tosun/ci-cd-for-dataflow-java-with-flex-templates-and-cloud-build-e3c584b8e564


## To launch the job locally :

- Copy the file from the project `gcs_input_file/input_teams_stats_raw.json` to the input bucket
- Create the `team_stat` `BigQuery` table, the script and the `BigQuery` schema are proposed in the `bigquery_table_scripts` folder


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
  --image "europe-west1-docker.pkg.dev/gb-poc-373711/internal-images/dataflow/team-league-python:latest" \
  --sdk-language "PYTHON" \
  --metadata-file "config/metadata.json"
```

# Run a Flex Template pipeline :

```bash
gcloud dataflow flex-template run "team-league-python-`date +%Y%m%d-%H%M%S`" \
    --template-file-gcs-location "gs://mazlum_dev/dataflow/templates/team_league/python/team-league-python.json" \
    --project=gb-poc-373711 \
    --region=europe-west1 \
    --temp-location=gs://mazlum_dev/dataflow/temp \
    --staging-location=gs://mazlum_dev/dataflow/staging \
    --parameters project_id=gb-poc-373711 \
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
    --config dataflow-deploy-template-dockerfile-all-dependencies.yaml \
    --substitutions _REPO_NAME="$REPO_NAME",_IMAGE_NAME="$IMAGE_NAME",_IMAGE_TAG="$IMAGE_TAG",_METADATA_TEMPLATE_FILE_PATH="$METADATA_TEMPLATE_FILE_PATH",_SDK_LANGUAGE="$SDK_LANGUAGE",_METADATA_FILE="$METADATA_FILE" \
    --verbosity="debug" .
```

### Run the Dataflow job with Cloud Build

```shell
gcloud builds submit \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --config dataflow-run-template.yaml \
    --substitutions _JOB_NAME="$JOB_NAME",_METADATA_TEMPLATE_FILE_PATH="$METADATA_TEMPLATE_FILE_PATH",_TEMP_LOCATION="$TEMP_LOCATION",_STAGING_LOCATION="$STAGING_LOCATION",_SA_EMAIL="$SA_EMAIL",_INPUT_FILE="$INPUT_FILE",_TEAM_LEAGUE_DATASET="$TEAM_LEAGUE_DATASET",_TEAM_STATS_TABLE="$TEAM_STATS_TABLE" \
    --verbosity="debug" .
```

# Deploy and run the template with Cloud Build with triggers

### Run unit tests with automatic trigger on Github repository

```bash
gcloud beta builds triggers create github \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --name="run-dataflow-unit-tests-python" \
    --repo-name=dataflow-python-ci-cd \
    --repo-owner=tosun-si \
    --branch-pattern=".*" \
    --build-config=dataflow-run-tests.yaml \
    --include-logs-with-status \
    --verbosity="debug"
```

### Build image from Dockerfile with all dependencies image and create spec file using a manual trigger on Github repository

```bash
gcloud beta builds triggers create manual \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --name="deploy-dataflow-template-team-league-python-dockerfile" \
    --repo="https://github.com/tosun-si/dataflow-python-ci-cd" \
    --repo-type="GITHUB" \
    --branch="main" \
    --build-config="dataflow-deploy-template-dockerfile-all-dependencies.yaml" \
    --substitutions _REPO_NAME="$REPO_NAME",_IMAGE_NAME="$IMAGE_NAME",_IMAGE_TAG="$IMAGE_TAG",_METADATA_TEMPLATE_FILE_PATH="$METADATA_TEMPLATE_FILE_PATH",_SDK_LANGUAGE="$SDK_LANGUAGE",_METADATA_FILE="$METADATA_FILE" \
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
    --build-config="dataflow-run-template.yaml" \
    --substitutions _JOB_NAME="$JOB_NAME",_METADATA_TEMPLATE_FILE_PATH="$METADATA_TEMPLATE_FILE_PATH",_TEMP_LOCATION="$TEMP_LOCATION",_STAGING_LOCATION="$STAGING_LOCATION",_SA_EMAIL="$SA_EMAIL",_INPUT_FILE="$INPUT_FILE",_TEAM_LEAGUE_DATASET="$TEAM_LEAGUE_DATASET",_TEAM_STATS_TABLE="$TEAM_STATS_TABLE" \
    --verbosity="debug"
```


# Build the image and create the Flex Template spec file with Dagger IO

Execute the script `export_env_variables.sh` : 

```bash
./scripts/export_env_variables.sh
```

Run the `build_image_and_spec_flex_template.go` script that build the Dockerfile and create the spec file in 
the Cloud Storage bucket for Flex Template : 

```
go run build_image_and_spec_flex_template.go
```

Run the `run_flex_template.go` script that run the Flex Template and the Dataflow job :

```
go run run_flex_template.go
```