#!/usr/bin/env bash

curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.1.2/docker-compose.yaml'

echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

docker-compose up airflow-init

echo ""

echo "Do you wish to install yq via brew for Linux / MacOS?"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) brew install yq; break;;
        No ) echo "You need to set your own GCP environment variables."; break;;
    esac
done

echo ""

set_gcp_env_variables_with_yq () {
    read -e -p "Enter your GCP_PROJECT_ID:" GCP_PROJECT_ID
    read -e -p "Enter your GCP_BIGQUERY_DATASET_NAME:" GCP_BIGQUERY_DATASET_NAME
    read -e -p "Enter your GCP_BIGQUERY_EXPORT_BUCKET_NAME:" GCP_BIGQUERY_EXPORT_BUCKET_NAME
    read -e -p "Enter your BIGQUERY_TABLE_NAME:" BIGQUERY_TABLE_NAME
    echo ""
    yq e -i '.x-airflow-common.environment.GCP_PROJECT_ID = "'$GCP_PROJECT_ID'"' docker-compose.yaml
    yq e -i '.x-airflow-common.environment.GCP_BIGQUERY_DATASET_NAME = "'$GCP_BIGQUERY_DATASET_NAME'"' docker-compose.yaml
    yq e -i '.x-airflow-common.environment.GCP_BIGQUERY_EXPORT_BUCKET_NAME = "'$GCP_BIGQUERY_EXPORT_BUCKET_NAME'"' docker-compose.yaml
    yq e -i '.x-airflow-common.environment.BIGQUERY_TABLE_NAME = "'$BIGQUERY_TABLE_NAME'"' docker-compose.yaml
    echo "Please check your docker-compose.yaml for Airflow, to see if your env variables are correctly set."
}

echo "Do you wish to set your own GCP environment variables with yq?"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) set_gcp_env_variables_with_yq; break;;
        No ) echo "Don't forget to set your GCP_PROJECT_ID, GCP_BIGQUERY_DATASET_NAME, GCP_BIGQUERY_EXPORT_BUCKET_NAME, BIGQUERY_TABLE_NAME environment variables within the docker-compose.yaml"; exit;;
    esac
done
