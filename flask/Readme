
# Flask Web Application

This Flask application is designed to manage and display patient data through a web interface. Below is a breakdown of the project structure and contents.

## Project Structure

- **`/` (root)**
  - `app.py`: The main Flask application file.
  - `requirements.txt`: Contains all Python dependencies required by the project.
  
- **`/database`**
  - SQL scripts for database operations:
    - `create_table.sql`: SQL script to create database tables.
    - `insert.sql`, `insert_sequence.sql`: Scripts for inserting initial data.
    - `cleaned_insert.sql`: Script for inserting cleaned data.
    - `create_patient_sequence.sql`: Script for creating sequence tables.
    - `patient_cases.db`: SQLite database file containing patient data.

- **`/static`**
  - Assets folder to serve static files.
    - `/css`
      - `bootstrap.min.css`: Minified Bootstrap CSS for styling.
    - `/js`
      - `bootstrap.bundle.min.js`, `bootstrap.min.js`: Bootstrap JavaScript files.
      - `intro.js`: Custom JavaScript logic.
    - `/macros`
      - Empty directory reserved for JavaScript macros or similar assets.

- **`/csv`**
  - Contains CSV files for data manipulation and upload.
    - `patient_data.csv`: Original patient data file.
    - `cleaned_patient_data.csv`: Cleaned version of patient data.
    - `full_sequence.csv`: Full sequence data file.

- **`/functions`**
  - Python scripts for data processing and functionality.
    - `convert_patient_data.py`: Script for converting patient data formats.
    - `cases_func.py`: Functions related to patient cases.
    - `load_balance.py`: Handles load balancing.
    - `sort_patients.py`: Sorts patient data.
    - `mapping.py`: Maps data fields to database fields.

- **`/templates`**
  - HTML templates for the web application.
    - `main.html`, `landing.html`, `upload.html`, `bed_counts.html`: HTML pages for different parts of the application.
    - `macros.html`: Template macros for reusable HTML components.

## Setup and Installation

1. Ensure Python 3.x is installed on your system.
2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Access the web application via `localhost:5000` in your browser.

## Usage

This application allows users to upload, view, and manage patient data through a series of web interfaces. Data can be uploaded via CSV files and managed through SQL database operations.

## Notes

- Modify SQL scripts in `/database` as per your schema requirements.
- Update `/static` and `/templates` to customize the look and functionality of the application.
- Extend functionality in `/functions` as needed for specific use cases.
