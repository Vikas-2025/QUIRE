# Quire: DICOM Metadata Pipeline

Quire is a lightweight pipeline for handling medical imaging data, specifically DICOM files. It supports data pulling from s3 as well as local, metadata extraction, and storage in a structured format, and provides basic reporting and visualizations.

---

## Features
- **Data Ingestion**: Download DICOM files from S3 or load from a local directory.
- **Metadata Extraction**: Extract key metadata such as Patient ID, Study Instance UID, Slice Thickness, and Pixel Spacing.
- **Data Storage**: Store metadata in a SQLite database with a structured schema.
- **Basic Reporting**: Generate summary statistics and visualizations of the dataset.

---

## Project Structure
```
Quire/
├── s3.py                # Handles S3 and local DICOM file downloading
├── download.py          # Orchestrates of whole pipeline ( main file to run s3 and local data,s3 process is commented)
├── process.py           # processin of downloded data and get metadata ( both s3 and local)
├── test.py              # Performs basic SQL operations and validations
├── .env                 # Environment variables (e.g., AWS credentials)
├── requirements.txt     # Python dependencies
├── dicom_metadata.db    # database
├── db.py                # Creation of database tables and Insertion of data into tables
└── visualization.ipynb  # Data Extraction from tables and perform basic EDA
```

---

## Prerequisites
- Python 3.8+
- Virtual environment setup (recommended)

---

## Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/Vikas-2025/QUIRE.git
cd QUIRE
```

### Step 2: Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
1. Rename `.env.example` to `.env`:
   ```bash
   mv .env.example .env
   ```
2. Update the `.env` file with your credentials and paths:
   ```env
   AWS_ACCESS_KEY=your-aws-access-key
   AWS_SECRET_KEY=your-aws-secret-key
   S3_BUCKET_NAME=your-s3-bucket-name
   S3_PREFIX=your-s3-prefix
   LOCAL_DICOM_DIR=./lidc_small_dset
   OUTPUT_DIR=./output_dicom
   DB_PATH=dicom_metadata.db
   LOCAL_DOWNLOAD_FROM_S3=./download
   ```

---

## Usage

### 1. Download Data
Download DICOM files from S3 or a local directory by running:
```bash
python download.py
```

### 2. Extract Metadata and Populate Database
Process DICOM files and store metadata in the SQLite database:
```bash
python process.py
```

### 3. Test and Query Data
Perform SQL operations and validate data:
```bash
python test.py
```

---

## Visualizations
Basic visualizations include:
1. **Total Number of Studies**
2. **Total Slices Across All Scans**
3. **Average Number of Slices per Study**
4. **Distribution of Slice Thickness**
5. **Gender Distribution in Patients**

Visualizations are automatically generated as part of the process script.

---

## Scalability
To handle 1,000+ scans:
- **Parallel Processing**: Use libraries like `multiprocessing` or `Dask` to parallelize metadata extraction.
- **Cloud Storage**: Migrate to cloud-based databases like AWS RDS or MongoDB Atlas for scalable storage.
- **Batch Processing**: Split datasets into manageable batches for efficient handling.

---

## Error Handling and Monitoring
- **Logging**: All errors are logged using Python's `logging` module.
- **Retry Mechanism**: Automatic retries for failed downloads or database inserts.
- **Alerts**: Integrate monitoring tools like AWS CloudWatch or Prometheus for error rate and throughput tracking.

---

## Database Schema

### DICOM Metadata Table
| Column               | Type   | Description                        |
|----------------------|--------|------------------------------------|
| `PatientID`          | TEXT   | Unique identifier for the patient |
| `StudyInstanceUID`   | TEXT   | Unique identifier for the study    |
| `SeriesInstanceUID`  | TEXT   | Unique identifier for the series   |
| `SliceThickness`     | REAL   | Thickness of the slice            |
| `PixelSpacing`       | TEXT   | Spacing between pixels            |
| `StudyDate`          | TEXT   | Date of the study                 |
| `Modality`           | TEXT   | Modality of the scan              |
| `Manufacturer`       | TEXT   | Manufacturer of the equipment     |


### Patient Table
| Column              | Type   | Description                        |
|---------------------|--------|------------------------------------|
| `patient_id`        | TEXT   | Unique identifier for the patient |
| `patient_name`      | TEXT   | Patient's name                    |
| `patient_birth_date`| TEXT   | Patient's birth date              |
| `patient_sex`       | TEXT   | Patient's gender                  |
| `last_menstrual_date`| TEXT  | Last menstrual date               |

### Study Table
| Column               | Type   | Description                        |
|----------------------|--------|------------------------------------|
| `study_instance_uid` | TEXT   | Unique identifier for the study    |
| `study_date`         | TEXT   | Date of the study                 |
| `study_time`         | TEXT   | Time of the study                 |
| `study_description`  | TEXT   | Study description                 |
| `patient_id`         | TEXT   | Foreign key to `Patient` table    |

### Series Table
| Column               | Type   | Description                        |
|----------------------|--------|------------------------------------|
| `series_instance_uid`| TEXT   | Unique identifier for the series   |
| `series_date`        | TEXT   | Date of the series                |
| `series_time`        | TEXT   | Time of the series                |
| `series_number`      | INTEGER| Number of the series              |
| `study_instance_uid` | TEXT   | Foreign key to `Study` table      |

---

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss the proposed changes.

---

## Contact
For questions or support, feel free to reach out to [Vikas Reddy](mailto:vikasreddy.bijivemula@gmail.com).

---

Let me know if you'd like me to tweak anything!

