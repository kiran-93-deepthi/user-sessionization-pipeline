
import hashlib
from datetime import timedelta, timezone

from django.db import transaction
from .models import Event, UserSession

SESSION_TIMEOUT_MINUTES = 30


def generate_session_id(user_id, first_event_id):
    value = f"{user_id}:{first_event_id}"
    return hashlib.sha256(value.encode()).hexdigest()[:32]


@transaction.atomic
def create_user_sessions():
    UserSession.objects.all().delete()

    user_ids = Event.objects.values_list(
        "user_id", flat=True
    ).distinct()

    for user_id in user_ids:
        events = list(
            Event.objects.filter(user_id=user_id)
            .order_by("event_time", "event_id")
        )

        if not events:
            continue

        current_events = [events[0]]

        for event in events[1:]:
            previous_event = current_events[-1]

            previous_time = previous_event.event_time.astimezone(timezone.utc)
            current_time = event.event_time.astimezone(timezone.utc)

            time_gap = current_time - previous_time

            if time_gap <= timedelta(minutes=SESSION_TIMEOUT_MINUTES):
                current_events.append(event)
            else:
                save_session(user_id, current_events)
                current_events = [event]

        save_session(user_id, current_events)


def save_session(user_id, events):
    first_event = events[0]

    session = UserSession.objects.create(
        session_id=generate_session_id(user_id, first_event.event_id),
        user_id=user_id,
        start_time=events[0].event_time,
        end_time=events[-1].event_time,
        event_count=len(events)
    )

    Event.objects.filter(
        id__in=[event.id for event in events]
    ).update(session=session)
