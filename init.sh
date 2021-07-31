#!/usr/bin/env bash

curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.1.2/docker-compose.yaml'

echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

docker-compose up airflow-init

echo "Don't forget to set your GCP_PROJECT_ID, GCP_BIGQUERY_DATASET_NAME, GCP_BIGQUERY_EXPORT_BUCKET_NAME environment variables within the docker-compose.yaml"
