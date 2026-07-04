from tracking.event_tracker import EventTracker
from monitor.file_monitor import FileEvent
from datetime import datetime


def make_event():
    return FileEvent(
        event_type="modified",
        path="test.txt",
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


def test_event_tracker_add():
    tracker = EventTracker()

    tracker.add_event(make_event())
    tracker.add_event(make_event())

    assert tracker.total_events() == 2


def test_event_type_count():
    tracker = EventTracker()

    tracker.add_event(make_event())

    counts = tracker.count_by_event_type()

    assert "modified" in counts