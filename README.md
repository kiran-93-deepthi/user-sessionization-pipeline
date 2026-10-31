# user-sessionization-pipeline
A Django-based data engineering pipeline for event processing and user sessionization.
# User Sessionization Data Engineering Pipeline

## Project Overview

The **User Sessionization Pipeline** is a Django-based data engineering project that transforms raw clickstream events into meaningful user sessions based on event timestamps.

The pipeline processes event data, handles out-of-order events, identifies duplicate records, validates timestamps, and groups user activities into sessions using a 30-minute inactivity threshold.

## Technologies Used

- Python
- Django
- SQLite
- HTML and CSS
- JavaScript
- CSV

## Key Features

- **CSV Upload:** Upload event data through the application.
- **Event Validation:** Validate user IDs, event IDs, and timestamps.
- **Duplicate Detection:** Identify duplicate event records.
- **Rejected Records:** Track invalid records and their rejection reasons.
- **Event-Time Processing:** Sort events chronologically, including out-of-order events.
- **Sessionization:** Group events into sessions using a 30-minute inactivity threshold.
- **Pipeline Tracking:** Maintain pipeline execution details and processing statistics.
- **Dashboard:** View processed sessions and pipeline information.

## Sessionization Logic

Events are grouped by user ID and sorted by event timestamp.

- If the time gap between consecutive events is 30 minutes or less, they belong to the same session.
- If the time gap is greater than 30 minutes, a new session is created.

## Project Structure

```text
user-sessionization-pipeline/
│
├── config/
├── sessionization/
├── sample_100_events.csv
├── requirements.txt
├── manage.py
└── README.md
```

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/kiran-93-deepthi/user-sessionization-pipeline.git
```

### 2. Open the project folder

```bash
cd user-sessionization-pipeline
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Start the Django server

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

## Sample Dataset

The repository includes `sample_100_events.csv` for testing the event-processing pipeline.

## Testing

Run automated tests using:

```bash
python manage.py test
```

## Author

**Swarna Kiran Deepthi**

GitHub: https://github.com/kiran-93-deepthi
