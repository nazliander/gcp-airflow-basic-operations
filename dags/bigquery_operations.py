import os
from airflow.models import DAG
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import (
    BigQueryToGCSOperator)
from airflow.providers.google.cloud.operators.gcs import (
    GCSDeleteObjectsOperator)
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from callable_functions.gcs_compose import compose_files_into_one


PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'bigquery-example')
DATASET_NAME = os.getenv('GCP_BIGQUERY_DATASET_NAME', 'bigquery-dataset')
DATA_EXPORT_BUCKET_NAME = os.getenv(
    'GCP_BIGQUERY_EXPORT_BUCKET_NAME', 'gcp-bucket')
TABLE = os.getenv('BIGQUERY_TABLE_NAME', 'bigquery-table')


with DAG(
    'gcp_dag',
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['example'],
) as dag:

    DS_NODASH = '{{ ds_nodash }}'
    EXPECTED_FILE_NAME = f'export-bigquery-{DS_NODASH}'

    bigquery_to_gcs = BigQueryToGCSOperator(
        gcp_conn_id='gcp_connection_id',
        task_id='bigquery_to_gcs',
        compression='GZIP',
        export_format='CSV',
        field_delimiter=',',
        print_header=False,
        source_project_dataset_table=f'{DATASET_NAME}.{TABLE}',
        destination_cloud_storage_uris=[
            f'gs://{DATA_EXPORT_BUCKET_NAME}/{EXPECTED_FILE_NAME}-*.csv.gz',
        ],
    )

    compose_files = PythonOperator(
        task_id='gcs_compose',
        python_callable=compose_files_into_one,
        op_kwargs={
            'bucket_name': DATA_EXPORT_BUCKET_NAME,
            'source_object_prefix': EXPECTED_FILE_NAME,
            'destination_object': f'{EXPECTED_FILE_NAME}.csv.gz',
            'gcp_conn_id': 'gcp_connection_id'
            },
    )

    delete_combined_objects = GCSDeleteObjectsOperator(
        task_id='gcs_combined_files_delete',
        gcp_conn_id='gcp_connection_id',
        bucket_name=DATA_EXPORT_BUCKET_NAME,
        prefix=f'{EXPECTED_FILE_NAME}-'
    )

    bigquery_to_gcs >> compose_files >> delete_combined_objects
