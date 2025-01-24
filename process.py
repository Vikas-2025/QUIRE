import logging
import boto3
import pydicom
from db import save_metadata_to_db
from organize import organize_output_folder
from s3 import download_s3_file, list_local_dicom_files, list_s3_dicom_files

import logging
import pydicom

def extract_metadata(dicom_file):
    """
    Extract metadata from a single DICOM file and ensure all lists are converted to strings.
    """
    try:
        dicom_data = pydicom.dcmread(dicom_file)
        
        # Function to handle list-like fields and PersonName fields
        def handle_list_field(field_name):
            field_value = dicom_data.get(field_name, "N/A")
            if isinstance(field_value, list) or isinstance(field_value, pydicom.multival.MultiValue):
                return ",".join(map(str, field_value))  # Convert list to a comma-separated string
            return field_value

        def handle_person_name(field_name):
            field_value = dicom_data.get(field_name, "N/A")
            if isinstance(field_value, pydicom.valuerep.PersonName):
                return str(field_value)  # Convert PersonName to string
            return field_value

        # Prepare the metadata dictionary with all values, ensuring list-like fields and PersonName fields are strings
        return {
            # Patient Information
            "PatientID": dicom_data.get("PatientID", "N/A"),
            "PatientName": handle_person_name("PatientName"),
            "PatientBirthDate": dicom_data.get("PatientBirthDate", "N/A"),
            "PatientSex": dicom_data.get("PatientSex", "N/A"),
            "LastMenstrualDate": dicom_data.get("LastMenstrualDate", "N/A"),
            
            # Study Information
            "StudyInstanceUID": dicom_data.get("StudyInstanceUID", "N/A"),
            "StudyDate": handle_list_field("StudyDate"),
            "StudyTime": dicom_data.get("StudyTime", "N/A"),
            "StudyDescription": dicom_data.get("StudyDescription", "N/A"),
            
            # Series Information
            "SeriesInstanceUID": dicom_data.get("SeriesInstanceUID", "N/A"),
            "SeriesDate": handle_list_field("SeriesDate"),
            "SeriesTime": dicom_data.get("SeriesTime", "N/A"),
            "SeriesNumber": dicom_data.get("SeriesNumber", "N/A"),
            
            # Additional Fields
            "SliceThickness": dicom_data.get("SliceThickness", "N/A"),
            "PixelSpacing": handle_list_field("PixelSpacing"),
            "Modality": dicom_data.get("Modality", "N/A"),
            "Manufacturer": dicom_data.get("Manufacturer", "N/A"),
        }
    except Exception as e:
        logging.error(f"Error reading DICOM file {dicom_file}: {e}")
        return None

def process_local_files(LOCAL_DICOM_DIR,OUTPUT_DIR):
    """
    Process DICOM files from a local directory.
    """
    dcm_files = list_local_dicom_files(LOCAL_DICOM_DIR)
    if not dcm_files:
        logging.error("No DICOM files found in the local directory.")
        return

    metadata_list = []
    for file_path in dcm_files:
        metadata = extract_metadata(file_path)
        if metadata:
            metadata_list.append(metadata)
            organize_output_folder(metadata, file_path,OUTPUT_DIR)

    if metadata_list:
        save_metadata_to_db(metadata_list)

def process_s3_files(S3_BUCKET_NAME, S3_PREFIX, AWS_ACCESS_KEY, AWS_SECRET_KEY,OUTPUT_DIR,LOCAL_DOWNLOAD_FROM_S3):
    """
    Process DICOM files stored in an S3 bucket with nested folders.
    """
    try:
        # Initialize S3 client
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

        # List all DICOM files in S3
        dcm_files = list_s3_dicom_files(S3_BUCKET_NAME, S3_PREFIX, s3_client)
        if not dcm_files:
            logging.error("No DICOM files found in the S3 bucket.")
            return

        # Download and process files
        metadata_list = []
        for s3_key in dcm_files:
            local_file_path = download_s3_file(S3_BUCKET_NAME, s3_key, LOCAL_DOWNLOAD_FROM_S3, s3_client)
            if local_file_path:
                metadata = extract_metadata(local_file_path)
                if metadata:
                    metadata_list.append(metadata)
                    organize_output_folder(metadata, local_file_path,OUTPUT_DIR)

        if metadata_list:
            save_metadata_to_db(metadata_list)
    except Exception as e:
        logging.error(f"Error processing S3 files: {e}")