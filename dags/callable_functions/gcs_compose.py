from airflow.providers.google.cloud.hooks.gcs import GCSHook


def compose_files_into_one(bucket_name: str,
                           source_object_prefix: str,
                           destination_object: str,
                           gcp_conn_id: str) -> None:
    '''Composes wildcarded files into one in the given destination'''
    gcs_hook = GCSHook(
        gcp_conn_id=gcp_conn_id
    )
    list_of_objects = gcs_hook.list(
        bucket_name,
        prefix=source_object_prefix
    )
    gcs_hook.compose(
        bucket_name,
        source_objects=list_of_objects,
        destination_object=destination_object
    )
