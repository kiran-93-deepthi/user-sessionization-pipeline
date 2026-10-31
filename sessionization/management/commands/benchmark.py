
import csv
import time

from django.core.management.base import BaseCommand

from sessionization.models import Event, PipelineRun, RejectedRecord
from sessionization.processor import create_user_sessions


class Command(BaseCommand):
    help = "Benchmark the sessionization pipeline"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="large_sample_events.csv"
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        start = time.perf_counter()

        # Count records in the CSV file
        with open(file_path, "r", encoding="utf-8-sig") as file:
            total_rows = sum(1 for row in csv.reader(file)) - 1

        # Start measuring session creation
        session_start = time.perf_counter()

        create_user_sessions()

        session_time = time.perf_counter() - session_start

        total_time = time.perf_counter() - start

        rate = (
            total_rows / total_time
            if total_time > 0 else 0
        )

        self.stdout.write(
            self.style.SUCCESS("Benchmark completed!")
        )

        self.stdout.write(f"CSV records: {total_rows}")
        self.stdout.write(f"Session creation time: {session_time:.2f} seconds")
        self.stdout.write(f"Total benchmark time: {total_time:.2f} seconds")
        self.stdout.write(f"Processing rate: {rate:.2f} events/second")
