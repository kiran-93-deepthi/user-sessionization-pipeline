
# User Sessionization Data Engineering Pipeline

## 1. Project Overview

This project transforms clickstream events into user sessions using a 30-minute inactivity timeout.

It is developed using Python and Django with SQLite as the database.

## 2. Features

- Upload clickstream events through a web dashboard.
- Read event data from CSV files.
- Handle out-of-order events by sorting them using event timestamps.
- Detect duplicate event IDs.
- Reject records with missing or invalid values.
- Validate timestamps and timezone information.
- Create user sessions using a 30-minute inactivity gap.
- Store events, sessions, rejected records, and pipeline run details.
- Display session results on a dashboard.
- Generate sample event data.
- Run automated tests.

## 3. Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS
- CSV
- Visual Studio Code

## 4. Sessionization Logic

Events are grouped by user ID and sorted by event timestamp.

If the time difference between consecutive events is 30 minutes or less, they belong to the same session.

If the time difference is greater than 30 minutes, a new session is created.

Example:

| Event | Time | Session |
|---|---|---|
| E001 | 09:00 | Session 1 |
| E002 | 09:15 | Session 1 |
| E003 | 09:30 | Session 1 |
| E004 | 10:05 | Session 2 |

## 5. Project Structure

```text
user-sessionization-django/
│
├── config/
│   ├── settings.py
│   └── urls.py
│
├── sessionization/
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── generate_events.py
│   ├── templates/
│   │   └── sessionization/
│   │       └── upload.html
│   ├── models.py
│   ├── processor.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── db.sqlite3
├── sample_events.csv
└── README.md
```

## 6. Installation

Install Python and Django.

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install Django:

```bash
pip install django
```

## 7. Database Setup

Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 8. Run the Project

```bash
python manage.py runserver
```

Open:

http://127.0.0.1:8000/

Upload a CSV file using the dashboard.

## 9. Generate Sample Data

Generate 100 events:

```bash
python manage.py generate_events --count 100 --output sample_100_events.csv
```

## 10. Run Automated Tests

```bash
python manage.py test sessionization
```

## 11. Expected Results

The dashboard displays:

- Total input records
- Inserted records
- Duplicate records
- Rejected records
- User session IDs
- Session start and end times
- Number of events in each session

## 12. Future Improvements

- Bulk database insertion for large CSV files.
- PostgreSQL database support.
- Improved pipeline performance.
- Docker deployment.
- REST API integration.

## 13. Author

Developed as a Data Engineering coding challenge project.
