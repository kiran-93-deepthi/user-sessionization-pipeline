
import csv
import random

from datetime import datetime, timedelta, timezone

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate sample clickstream events"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=100000,
            help="Number of events to generate"
        )

        parser.add_argument(
            "--output",
            type=str,
            default="large_sample_events.csv",
            help="Output CSV filename"
        )

    def handle(self, *args, **options):
        count = options["count"]
        output = options["output"]

        if count <= 0:
            self.stderr.write("Event count must be greater than zero.")
            return

        random.seed(42)

        users = [f"U{i:05d}" for i in range(1, 1001)]

        event_types = [
            "page_view",
            "button_click",
            "search",
            "product_view",
            "add_to_cart",
            "checkout",
            "logout"
        ]

        start_time = datetime(
            2026, 10, 30, 0, 0, 0,
            tzinfo=timezone.utc
        )

        with open(output, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "event_id",
                "user_id",
                "event_time",
                "event_type"
            ])

            for i in range(1, count + 1):
                user_id = random.choice(users)

                event_time = start_time + timedelta(
                    seconds=random.randint(0, 86400)
                )

                event_type = random.choice(event_types)

                writer.writerow([
                    f"EVT{i:07d}",
                    user_id,
                    event_time.isoformat().replace("+00:00", "Z"),
                    event_type
                ])

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully generated {count} events in {output}"
            )
        )
