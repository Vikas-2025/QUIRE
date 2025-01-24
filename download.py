import os
import logging
from process import process_local_files, process_s3_files
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Local directory configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_PREFIX = os.getenv("S3_PREFIX")
LOCAL_DICOM_DIR = os.getenv("LOCAL_DICOM_DIR")
LOCAL_DOWNLOAD_FROM_S3 =  os.getenv("LOCAL_DOWNLOAD_FROM_S3")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
DB_PATH = os.getenv("DB_PATH")

# Create Directorys if not exist
os.makedirs(LOCAL_DICOM_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOCAL_DOWNLOAD_FROM_S3, exist_ok=True)

def main():
    process_local_files(LOCAL_DICOM_DIR,OUTPUT_DIR)
    # Uncomment and provide AWS credentials for S3 processing
    # process_s3_files(S3_BUCKET_NAME, S3_PREFIX, AWS_ACCESS_KEY, AWS_SECRET_KEY,OUTPUT_DIR,LOCAL_DOWNLOAD_FROM_S3)

if __name__ == "__main__":
    main()
