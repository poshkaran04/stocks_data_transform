import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.contrib.operators.gcs_list_operator import GoogleCloudStorageListOperator

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'us_stocks')

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

dag = DAG(
    'load_stocks_data_usa',
    default_args=default_args,
    schedule_interval=None,
)

# Hardcoded - Please change as per your own configuration
GCS_FOLDER = 'gs://bootcamp_data_lake_data-bootcamp-380922/Stocks/'
GCS_DELIMITER = ','
GCS_QUOTECHAR = '"'
BQ_PROJECT = PROJECT_ID
BQ_DATASET = 'us_stocks'
BQ_TABLE = 'stocks_data_usa'
file_pattern = 'Stocks/*.csv'


# Define the GCS bucket and folder where the input files are located
gcs_bucket = BUCKET
folder = 'Stocks'

# Define the GoogleCloudStorageListOperator to get the list of input files
get_file_list = GoogleCloudStorageListOperator(
    task_id='get_file_list',
    bucket=gcs_bucket,
    prefix=folder,
    delimiter='.txt',
    dag=dag,
)

# Define the GCS to BigQuery operator
gcs_to_bq = GoogleCloudStorageToBigQueryOperator(
    task_id='gcs_to_bq',
    bucket=BUCKET,
    source_objects=[file_pattern],
    destination_project_dataset_table=f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}",
    schema_fields=[
        {'name': 'filename', 'type': 'STRING'},
        {'name': 'date', 'type': 'DATE'},
        {'name': 'open', 'type': 'FLOAT'},
        {'name': 'high', 'type': 'FLOAT'},
        {'name': 'low', 'type': 'FLOAT'},
        {'name': 'close', 'type': 'FLOAT'},
        {'name': 'volume', 'type': 'INTEGER'},
        {'name': 'OpenInt', 'type': 'INTEGER'},
    ],
    # write_disposition='WRITE_TRUNCATE',
    skip_leading_rows=1,
    autodetect=False,
    allow_jagged_rows=True,
    allow_quoted_newlines=True,
    ignore_unknown_values=False,
    dag=dag,
)


get_file_list >> gcs_to_bq
