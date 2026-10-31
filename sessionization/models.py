
import uuid

from django.db import models


class PipelineRun(models.Model):
    run_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, default="running")

    input_count = models.PositiveIntegerField(default=0)
    inserted_count = models.PositiveIntegerField(default=0)
    duplicate_count = models.PositiveIntegerField(default=0)
    rejected_count = models.PositiveIntegerField(default=0)

    source_file = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.run_id)


class UserSession(models.Model):
    session_id = models.CharField(max_length=64, unique=True)
    user_id = models.CharField(max_length=100)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.session_id


class Event(models.Model):
    event_id = models.CharField(max_length=100, unique=True)
    user_id = models.CharField(max_length=100)
    event_time = models.DateTimeField()
    event_type = models.CharField(max_length=100)

    source_file = models.CharField(max_length=255)
    run = models.ForeignKey(
        PipelineRun,
        on_delete=models.PROTECT,
        related_name="events"
    )
    session = models.ForeignKey(
        UserSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events"
    )

    def __str__(self):
        return self.event_id


class RejectedRecord(models.Model):
    run = models.ForeignKey(
        PipelineRun,
        on_delete=models.CASCADE,
        related_name="rejected_records"
    )
    source_file = models.CharField(max_length=255)
    row_number = models.PositiveIntegerField()
    raw_data = models.TextField()
    reason = models.TextField()

    def __str__(self):
        return f"Rejected row {self.row_number}"
