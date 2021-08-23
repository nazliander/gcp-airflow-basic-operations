# Example GCP and Airflow operations

Includes:

- **BigQueryToGCSOperator:** To export tables into Google Cloud Storage (example is with partitions).

- **PythonOperator:** Leveraging GoogleCloudStorageHook in a custom function to compose partition text files into one file.

- **GCSDeleteObjectsOperator:** To delete objects from a given bucket and prefix.


## Running locally:

Initialize the Airflow in Docker. It will ask you about installing [yq](https://github.com/mikefarah/yq) in your Linux/Mac development environment:

```bash
./init.sh
```

If you don't want to use an external tool to edit your docker-compose, please set your GCP_PROJECT_ID, GCP_BIGQUERY_DATASET_NAME, GCP_BIGQUERY_EXPORT_BUCKET_NAME, BIGQUERY_TABLE_NAME environment variables manually. This is possible by add those lines on the `docker-compose.yaml` `x-airflow-common` service environment:

```
    GCP_PROJECT_ID: '<YOUR-PROJECT-ID>'
    GCP_BIGQUERY_DATASET_NAME: '<YOUR-DATASET>'
    GCP_BIGQUERY_EXPORT_BUCKET_NAME: '<YOUR-BUCKET-NAME>'
    BIGQUERY_TABLE_NAME: '<YOUR-TABLE-NAME>'
```

```bash
docker-compose up
```

Then go to [local Airflow.](http://0.0.0.0:8080/)

Go to the configurations to set up your GCP Connection. Please follow [the instructions on the providers documentation.](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/connections/gcp.html)

![Connection to GCS](screenshots/connection.png)

Run the DAGs on demand and see the pipeline running.

![Running DAG](screenshots/running_dag.png)
