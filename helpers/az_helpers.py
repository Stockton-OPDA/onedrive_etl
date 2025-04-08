import os
import pandas as pd
from azure.storage.blob import BlobServiceClient
import logging

logger = logging.getLogger(__name__)

def upload_to_adls(data: pd.DataFrame, connectionString: str, containerName: str, blob_name: str) -> None:
    """
    Uploads the given data to Azure Blob Storage in Parquet format.

    Parameters:
        data (pd.DataFrame): The data to be uploaded.
        connectionString (str): Azure Blob Storage connection string.
        containerName (str): The name of the container to upload the data to.
        blobName (str): The name of the blob to create in the container.
        parquet_file_path (str): The path of the Parquet file to save to.

    Returns:
        None
    """
    try:
        # Configure reports directory
        report_directory = 'reports'
        if not os.path.exists(report_directory):
            os.makedirs(report_directory)

        # Connect to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(connectionString)
        container_client = blob_service_client.get_container_client(containerName)
        
        # Check if the container exists, create if not
        if not container_client.exists():
            container_client.create_container()
            logger.info(f"Container '{containerName}' created successfully.")

        blob_client = container_client.get_blob_client(blob_name)
    
        # Upload Parquet file to Azure Blob Storage
        parquet_file_path = f'reports/{blob_name}'
        data.to_parquet(path=parquet_file_path, index=False)

        with open(parquet_file_path, "rb") as data_file:
            blob_client.upload_blob(data_file, overwrite=True)
        logger.info("Parquet file successfully uploaded to Azure Blob Storage.")
    
    except Exception as e:
        logger.error("An error occurred during blob upload: %s", str(e))