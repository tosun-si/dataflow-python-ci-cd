#!/usr/bin/env bash

set -e
set -o pipefail
set -u

export PROJECT_ID=gb-poc-373711
export LOCATION=europe-west1

export REPO_NAME=internal-images
export IMAGE_NAME="dataflow/team-league-python-dagger"
export IMAGE_TAG=latest
export METADATA_FILE="config/metadata.json"
export METADATA_TEMPLATE_FILE_PATH="gs://mazlum_dev/dataflow/templates/team_league/python/team-league-python.json"
export SDK_LANGUAGE=PYTHON
export JOB_NAME="team-league-python-dagger"
export TEMP_LOCATION=gs://mazlum_dev/dataflow/temp
export STAGING_LOCATION="gs://mazlum_dev/dataflow/staging"

export SA_EMAIL=sa-dataflow-dev@gb-poc-373711.iam.gserviceaccount.com
export INPUT_FILE="gs://mazlum_dev/team_league/input/json/input_teams_stats_raw.json"
export SIDE_INPUT_FILE="gs://mazlum_dev/team_league/input/json/input_team_slogans.json"
export TEAM_LEAGUE_DATASET=mazlum_test
export TEAM_STATS_TABLE=team_stat
