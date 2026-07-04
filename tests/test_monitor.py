from monitor.file_monitor import FileEvent


def test_file_event_creation():
    event = FileEvent(
        event_type="created",
        path="./watched/test.txt",
        timestamp="2026-07-04 12:00:01",
    )

    assert event.event_type == "created"
    assert "test.txt" in event.path
    assert isinstance(event.timestamp, str)