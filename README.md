#DICOM Metadata Pipeline
##Overview
This project processes a subset of 10-15 CT scans in DICOM format from the LIDC-IDRI dataset. The pipeline downloads the scans (from a local directory or an S3 bucket), extracts relevant metadata from the DICOM headers, organizes the data, stores it in an SQLite database, and generates basic data summaries and visualizations.
##Features
**Data Ingestion:**

Downloads DICOM files programmatically from an S3 bucket or a local directory.
Handles folder structures with multiple DICOM files per study.
Includes error handling for corrupted or missing files.
**Metadata Extraction:**

Extracts metadata fields like Patient ID, Study Instance UID, Series Instance UID, Slice Thickness, and more.
Supports a logical folder structure: <PatientID>/<StudyInstanceUID>/<SeriesInstanceUID>.
Data Storage:

Stores extracted metadata in an SQLite database with a normalized schema (tables for patients, studies, and series).
**Reporting & Visualization:**

Generates summary statistics:
Total number of studies and slices.
Average slices per study.
Distribution of slice thickness.
Includes optional visualizations using Matplotlib and Seaborn.
