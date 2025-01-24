import logging
import os


def download_s3_file(bucket_name, s3_key, local_path, s3_client):
    """
    Download a file from S3 to a local path.
    """
    try:
        local_file_path = os.path.join(local_path, os.path.basename(s3_key))
        s3_client.download_file(bucket_name, s3_key, local_file_path)
        return local_file_path
    except Exception as e:
        logging.error(f"Error downloading file {s3_key} from S3: {e}")
        return None
    
def list_s3_dicom_files(bucket_name, prefix, s3_client):
    """
    List all .dcm files in an S3 bucket under a specific prefix, including nested folders.
    """
    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        operation_parameters = {"Bucket": bucket_name, "Prefix": prefix}
        dcm_files = []

        for page in paginator.paginate(**operation_parameters):
            for obj in page.get("Contents", []):
                if obj["Key"].endswith(".dcm"):  # Only add .dcm files
                    dcm_files.append(obj["Key"])
        
        return dcm_files
    except Exception as e:
        logging.error(f"Error listing DICOM files from S3: {e}")
        return []
    
def list_local_dicom_files(directory):
    """
    Recursively list all .dcm files in the specified local directory, including nested folders.
    """
    try:
        dcm_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".dcm"):
                    dcm_files.append(os.path.join(root, file))
        return dcm_files
    except Exception as e:
        logging.error(f"Error listing DICOM files: {e}")
        return []

