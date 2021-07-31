# Example GCP and Airflow operations

Includes:

- **BigQueryToGCSOperator:** To export tables into Google Cloud Storage (example is with partitions).

- **PythonOperator:** To leverage GoogleCloudStorageHook in a custom function.

- **GCSDeleteObjectsOperator:** To delete objects from a given bucket and prefix.


## Running locally:

Initialize the Airflow in Docker:

```bash
./init.sh
```

To set your GCP_PROJECT_ID, GCP_BIGQUERY_DATASET_NAME, GCP_BIGQUERY_EXPORT_BUCKET_NAME environment variables, add those lines on the docker-compose.yaml airflow-common service environment:

```
    GCP_PROJECT_ID: '<YOUR-PROJECT-ID>'
    GCP_BIGQUERY_DATASET_NAME: '<YOUR-DATASET>'
    GCP_BIGQUERY_EXPORT_BUCKET_NAME: '<YOUR-BUCKET-NAME>'
```

```bash
docker-compose up
```

Then go to [local Airflow.](http://0.0.0.0:8080/)

Run the DAGs on demand and see the pipeline running.
