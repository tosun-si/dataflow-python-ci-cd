#!/usr/bin/env bash

set -e
set -o pipefail
set -u

echo "#######Building Dataflow Docker image"

gcloud builds submit --tag "$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:$IMAGE_TAG" .

echo "#######Creating Dataflow Flex Template"

gcloud dataflow flex-template build "$METADATA_TEMPLATE_FILE_PATH" \
  --image-gcr-path "$LOCATION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:$IMAGE_TAG" \
  --sdk-language "$SDK_LANGUAGE" \
  --flex-template-base-image "$FLEX_TEMPLATE_BASE_IMAGE" \
  --metadata-file "$METADATA_FILE" \
  --py-path "$PY_PATH" \
  --env "FLEX_TEMPLATE_PYTHON_PY_FILE=$FLEX_TEMPLATE_PYTHON_PY_FILE" \
  --env "FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE=$FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE" \
  --env "FLEX_TEMPLATE_PYTHON_SETUP_FILE=setup.py"
