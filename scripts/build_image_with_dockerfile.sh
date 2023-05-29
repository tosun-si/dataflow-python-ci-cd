#!/usr/bin/env bash

set -e
set -o pipefail
set -u

echo "#######Building Dataflow Flex Template Docker image with all the dependencies installed inside"

gcloud builds submit --tag "$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:$IMAGE_TAG" .
