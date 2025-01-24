import logging
import os
import shutil

import pydicom


def organize_output_folder(metadata, source_path,OUTPUT_DIR):
    """
    Create folder structure <PatientID>/<StudyInstanceUID>/ and save the latest file by StudyDate.
    """
    try:
        patient_id = metadata["PatientID"]
        study_uid = metadata["StudyInstanceUID"]
        study_date = metadata["StudyDate"]

        if patient_id == "N/A" or study_uid == "N/A" or study_date == "N/A":
            logging.warning(f"Skipping file {source_path} due to missing metadata.")
            return

        # Create directory structure
        output_path = os.path.join(OUTPUT_DIR, patient_id, study_uid)
        os.makedirs(output_path, exist_ok=True)

        # Destination file path
        file_name = os.path.basename(source_path)
        destination_file = os.path.join(output_path, file_name)

        # Replace file only if it's newer
        if os.path.exists(destination_file):
            existing_file = pydicom.dcmread(destination_file)
            existing_study_date = existing_file.get("StudyDate", "N/A")

            if study_date > existing_study_date:
                shutil.copy2(source_path, destination_file)
                logging.info(f"Replaced older file at {destination_file} with newer StudyDate {study_date}.")
            else:
                pass
        else:
            shutil.copy2(source_path, destination_file)
    except Exception as e:
        logging.error(f"Error organizing output folder for file {source_path}: {e}")
