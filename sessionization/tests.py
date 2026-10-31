from django.test import TestCase


from datetime import datetime, timezone as dt_timezone

from django.test import TestCase

from .models import Event, PipelineRun, UserSession
from .processor import create_user_sessions


class SessionizationTests(TestCase):

    def setUp(self):
        self.run = PipelineRun.objects.create(
            status="completed",
            source_file="test.csv"
        )

    def add_event(self, event_id, user_id, event_time):
        Event.objects.create(
            event_id=event_id,
            user_id=user_id,
            event_time=datetime.fromisoformat(
                event_time.replace("Z", "+00:00")
            ),
            event_type="page_view",
            source_file="test.csv",
            run=self.run
        )

    def test_events_within_30_minutes_same_session(self):
        self.add_event("E1", "U1", "2026-10-30T09:00:00Z")
        self.add_event("E2", "U1", "2026-10-30T09:30:00Z")

        create_user_sessions()

        self.assertEqual(UserSession.objects.count(), 1)

        session = UserSession.objects.first()
        self.assertEqual(session.event_count, 2)

    def test_gap_more_than_30_minutes_new_session(self):
        self.add_event("E1", "U1", "2026-10-30T09:00:00Z")
        self.add_event("E2", "U1", "2026-10-30T09:31:00Z")

        create_user_sessions()

        self.assertEqual(UserSession.objects.count(), 2)

   
    
    def test_out_of_order_events(self):
        self.add_event("E1", "U1", "2026-10-30T10:00:00Z")
        self.add_event("E2", "U1", "2026-10-30T09:00:00Z")
        self.add_event("E3", "U1", "2026-10-30T09:20:00Z")

        create_user_sessions()

        self.assertEqual(UserSession.objects.count(), 2)

        sessions = UserSession.objects.filter(
            user_id="U1"
        ).order_by("start_time")

        self.assertEqual(sessions[0].event_count, 2)
        self.assertEqual(sessions[1].event_count, 1)


    def test_multiple_users(self):
        self.add_event("E1", "U1", "2026-10-30T09:00:00Z")
        self.add_event("E2", "U2", "2026-10-30T09:05:00Z")

        create_user_sessions()

        self.assertEqual(UserSession.objects.count(), 2)

    def test_single_event_session(self):
        self.add_event("E1", "U1", "2026-10-30T09:00:00Z")

        create_user_sessions()

        self.assertEqual(UserSession.objects.count(), 1)

        session = UserSession.objects.first()
        self.assertEqual(session.event_count, 1)
# Create your tests here.
