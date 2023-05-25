#!/usr/bin/env bash

set -e
set -o pipefail
set -u

gcloud auth activate-service-account --key-file "${GOOGLE_APPLICATION_CREDENTIALS}"
gcloud config set project "$GCP_PROJECT_ID"
