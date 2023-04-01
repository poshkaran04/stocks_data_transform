import os
import csv
import logging
from datetime import datetime, timedelta
import zipfile

# airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi

# gcp
from google.cloud import storage

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

# Hardcoded - Please change as per your own configuration
LOCAL_FOLDER_PATH = '/opt/airflow/Stocks/'
GCS_FOLDER_PATH = 'Stocks'
BUCKET_NAME = 'bootcamp_data_lake_data-bootcamp-380922'

KAGGLE_USERNAME = os.environ.get("KG_USERNAME")
KAGGLE_KEY = os.environ.get("KG_KEY")


def upload_to_gcs():
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)

    for subdir, _, files in os.walk(LOCAL_FOLDER_PATH):
        for file in files:
            local_file_path = os.path.join(subdir, file)
            gcs_file_path = os.path.join(GCS_FOLDER_PATH, local_file_path.replace(
                LOCAL_FOLDER_PATH, '', 1).lstrip('/'))
            # gcs_file_path = os.path.join(gcs_folder_path, local_file_path[len(local_folder_path)+1:])
            blob = bucket.blob(gcs_file_path)
            blob.upload_from_filename(local_file_path)


def convert_text_to_csv(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r') as f:
                lines = f.readlines()
                csv_filepath = os.path.splitext(filepath)[0] + '.csv'
                with open(csv_filepath, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    if len(lines) > 0:
                        writer.writerow(
                            ['Filename'] + lines[0].strip().split(','))
                        for line in lines[1:]:
                            row = [filename] + line.strip().split(',')
                            writer.writerow(row)
            os.remove(filepath)


default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 3, 26),
    "depends_on_past": False,
    "retries": 1,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
        dag_id="kaggle_extract",
        schedule_interval="@daily",
        default_args=default_args,
        catchup=False,
        max_active_runs=1,
        tags=['dtc-de'],
) as dag:
    # Define the Kaggle dataset you want to download
    dataset_name = 'borismarjanovic/price-volume-data-for-all-us-stocks-etfs'

    # Set the path where the dataset will be downloaded
    path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

    # Define the BashOperator to extract the dataset
    download_dataset = BashOperator(
        task_id='download_dataset',
        bash_command=f'kaggle datasets download -d {dataset_name} -p {path_to_local_home}'
    )

    unzip_dataset = BashOperator(task_id='unzip_dataset',
                                 # Comment after 1st Run
                                 bash_command=f'unzip -o {path_to_local_home}/*zip -d {path_to_local_home}'
                                 # Uncomment After 1st Run
                                 # bash_command=f'if [ ! -d "{path_to_local_home}" ]; then unzip {path_to_local_home} -d {path_to_local_home}; fi'
                                 )

    convert_text_to_csv_task = PythonOperator(
        task_id='convert_text_to_csv',
        python_callable=convert_text_to_csv,
        op_kwargs={'folder_path': local_folder_path},
        dag=dag,
    )

    upload_to_gcs = PythonOperator(
        task_id="upload_to_gcs",
        python_callable=upload_to_gcs,
    )

    # Set the dependencies of the DAG
    download_dataset >> unzip_dataset >> convert_text_to_csv_task >> upload_to_gcs
