

import csv
import io
from datetime import datetime

from django.shortcuts import render
from django.utils import timezone

from .models import PipelineRun, Event, RejectedRecord, UserSession
from .processor import create_user_sessions


def upload_events(request):
    message = ""

    if request.method == "POST":
        uploaded_file = request.FILES.get("event_file")

        if not uploaded_file:
            message = "Please select a CSV file."

        else:
            try:
                # Read CSV file
                uploaded_file.seek(0)
                content = uploaded_file.read().decode("utf-8-sig")

                reader = csv.reader(io.StringIO(content))
                rows = list(reader)

                # Remove empty rows
                rows = [
                    row for row in rows
                    if any(cell.strip() for cell in row)
                ]

                if not rows:
                    raise ValueError("CSV file is empty.")

                # Read CSV headers
                headers = [
                    column.strip().lower().replace(" ", "_")
                    for column in rows[0]
                ]

                required_columns = [
                    "event_id",
                    "user_id",
                    "event_time",
                    "event_type"
                ]

                if not all(column in headers for column in required_columns):
                    raise ValueError(
                        f"Invalid CSV headers. Found: {headers}"
                    )

                column_index = {
                    column: headers.index(column)
                    for column in required_columns
                }

                # Create pipeline run
                run = PipelineRun.objects.create(
                    source_file=uploaded_file.name,
                    status="running"
                )

                inserted = 0
                duplicates = 0
                rejected = 0

                # Process CSV records
                for row_number, row in enumerate(rows[1:], start=2):
                    run.input_count += 1

                    try:
                        if len(row) < len(headers):
                            raise ValueError("Missing column values.")

                        event_id = row[column_index["event_id"]].strip()
                        user_id = row[column_index["user_id"]].strip()
                        event_time_text = row[column_index["event_time"]].strip()
                        event_type = row[column_index["event_type"]].strip()

                        if not all([
                            event_id,
                            user_id,
                            event_time_text,
                            event_type
                        ]):
                            raise ValueError("Required values are missing.")

                        event_time = datetime.fromisoformat(
                            event_time_text.replace("Z", "+00:00")
                        )

                        if timezone.is_naive(event_time):
                            raise ValueError(
                                "Timestamp must include a timezone."
                            )

                        # Check duplicate event
                        if Event.objects.filter(event_id=event_id).exists():
                            duplicates += 1
                            continue

                        # Save event
                        Event.objects.create(
                            event_id=event_id,
                            user_id=user_id,
                            event_time=event_time,
                            event_type=event_type,
                            source_file=uploaded_file.name,
                            run=run
                        )

                        inserted += 1

                    except Exception as error:
                        rejected += 1

                        RejectedRecord.objects.create(
                            run=run,
                            source_file=uploaded_file.name,
                            row_number=row_number,
                            raw_data=",".join(row),
                            reason=str(error)
                        )

                # Save pipeline metrics
                run.inserted_count = inserted
                run.duplicate_count = duplicates
                run.rejected_count = rejected
                run.status = "completed"
                run.finished_at = timezone.now()
                run.save()

                # Create user sessions
                create_user_sessions()

                message = (
                    f"Upload successful! "
                    f"Total rows: {run.input_count}, "
                    f"Inserted: {inserted}, "
                    f"Duplicates: {duplicates}, "
                    f"Rejected: {rejected}. "
                    f"User sessions created successfully."
                )

            except Exception as error:
                message = f"Upload failed: {str(error)}"

    # Get sessions for displaying on website
    sessions = UserSession.objects.all().order_by(
        "user_id", "start_time"
    )

    # Get session results
    sessions = UserSession.objects.all().order_by(
        "user_id", "start_time"
    )

    # Get pipeline run history
    runs = PipelineRun.objects.all().order_by("-started_at")

    return render(
        request,
        "sessionization/upload.html",
        {
            "message": message,
            "sessions": sessions,
            "runs": runs
        }
    )

    return render(
        request,
        "sessionization/upload.html",
        {
            "message": message,
            "sessions": sessions
        }
    )
