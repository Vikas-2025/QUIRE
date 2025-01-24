import logging
import sqlite3

def save_metadata_to_db(metadata_list):
    """
    Save extracted metadata to an SQLite database. Avoid duplicates by checking existing records.
    """
    try:
        conn = sqlite3.connect('dicom_metadata.db')
        cursor = conn.cursor()

        # Create the table if it doesn't already exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dicom_metadata (
                PatientID TEXT,
                StudyInstanceUID TEXT,
                SeriesInstanceUID TEXT,
                SliceThickness REAL,
                PixelSpacing TEXT,
                StudyDate TEXT,
                Modality TEXT,
                Manufacturer TEXT,
                UNIQUE(PatientID, StudyInstanceUID, SeriesInstanceUID)  -- Unique constraint to prevent duplicates
            )
        """)
        conn.commit()

        # Insert metadata into the dicom_metadata table with conflict resolution (ignore duplicates)
        cursor.executemany("""
            INSERT OR IGNORE INTO dicom_metadata (
                PatientID, StudyInstanceUID, SeriesInstanceUID,
                SliceThickness, PixelSpacing, StudyDate, Modality, Manufacturer
            ) VALUES (
                :PatientID, :StudyInstanceUID, :SeriesInstanceUID,
                :SliceThickness, :PixelSpacing, :StudyDate, :Modality, :Manufacturer
            )
        """, metadata_list)
        conn.commit()

        # Insert data into the Patient, Study, and Series tables
        for metadata in metadata_list:
            # Insert data into the Patient table
            cursor.execute('''
                INSERT OR IGNORE INTO Patient (
                    patient_id, patient_name, patient_birth_date, patient_sex, last_menstrual_date
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                metadata.get("PatientID"),
                metadata.get("PatientName"),
                metadata.get("PatientBirthDate"),
                metadata.get("PatientSex"),
                metadata.get("LastMenstrualDate")
            ))

            # Insert data into the Study table
            cursor.execute('''
                INSERT OR IGNORE INTO Study (
                    study_instance_uid, study_date, study_time, study_description, patient_id
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                metadata.get("StudyInstanceUID"),
                metadata.get("StudyDate"),
                metadata.get("StudyTime"),
                metadata.get("StudyDescription"),
                metadata.get("PatientID")  # Foreign key reference to Patient table
            ))

            # Insert data into the Series table
            cursor.execute('''
                INSERT OR IGNORE INTO Series (
                    series_instance_uid, series_date, series_time, series_number, study_instance_uid
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                metadata.get("SeriesInstanceUID"),
                metadata.get("SeriesDate"),
                metadata.get("SeriesTime"),
                metadata.get("SeriesNumber"),
                metadata.get("StudyInstanceUID")  # Foreign key reference to Study table
            ))

        conn.commit()

        logging.info("Metadata saved to database.")
        conn.close()
    except Exception as e:
        logging.error("Error saving metadata to database: %s", e)


# import sqlite3

# # Connect to the SQLite database (or create it if it doesn't exist)
# conn = sqlite3.connect('dicom_metadata.db')
# cursor = conn.cursor()

# # Create the Patient table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Patient (
#     patient_id TEXT PRIMARY KEY,  -- Patient ID as the primary key
#     patient_name TEXT,
#     patient_birth_date TEXT,
#     patient_sex TEXT,
#     last_menstrual_date TEXT
# );
# ''')

# # Create the Study table with a foreign key reference to the Patient table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Study (
#     study_instance_uid TEXT PRIMARY KEY,  -- Study Instance UID as the primary key
#     study_date TEXT,
#     study_time TEXT,
#     study_description TEXT,
#     patient_id TEXT,  -- Foreign key reference to the Patient table
#     FOREIGN KEY (patient_id) REFERENCES Patient (patient_id)
# );
# ''')

# # Create the Series table with a foreign key reference to the Study table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Series (
#     series_instance_uid TEXT PRIMARY KEY,  -- Series Instance UID as the primary key
#     series_date TEXT,
#     series_time TEXT,
#     series_number INTEGER,
#     study_instance_uid TEXT,  -- Foreign key reference to the Study table
#     FOREIGN KEY (study_instance_uid) REFERENCES Study (study_instance_uid)
# );
# ''')

# # Commit changes and close the connection
# conn.commit()

# # Close the connection
# conn.close()

# print("Tables created successfully.")

