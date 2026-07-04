"""
tracking/event_tracker.py

Tracks filesystem events over time to compute:
- event rates
- per-type counts
- sliding window bursts

This is useful for behavioral analysis in monitoring systems.
"""

from collections import defaultdict, deque
from datetime import datetime, timedelta


class EventTracker:
    """
    Tracks file system events in memory.
    """

    def __init__(self, window_seconds=60):

        self.window = timedelta(seconds=window_seconds)

        # stores (timestamp, event_type, path)
        self.events = deque()

        self.count_by_type = defaultdict(int)

    # ----------------------------------------------------
    # Add event
    # ----------------------------------------------------

    def add_event(self, event):
        """
        Add a FileEvent to the tracker.
        """

        timestamp = self._parse_timestamp(event.timestamp)

        self.events.append(
            (timestamp, event.event_type, event.path)
        )

        self.count_by_type[event.event_type] += 1

        self._cleanup(timestamp)

    # ----------------------------------------------------
    # Cleanup old events
    # ----------------------------------------------------

    def _cleanup(self, current_time):

        while self.events:

            oldest_time = self.events[0][0]

            if current_time - oldest_time > self.window:
                old = self.events.popleft()

                # decrement counts safely
                self.count_by_type[old[1]] -= 1

                if self.count_by_type[old[1]] <= 0:
                    del self.count_by_type[old[1]]

            else:
                break

    # ----------------------------------------------------
    # Metrics
    # ----------------------------------------------------

    def total_events(self):
        return len(self.events)

    def event_rate_per_minute(self):
        """
        Approximate events per minute in current window.
        """

        seconds = self.window.total_seconds()

        if seconds == 0:
            return 0

        return (len(self.events) / seconds) * 60

    def count_by_event_type(self):
        """
        Return current counts per event type.
        """

        return dict(self.count_by_type)

    def most_active_paths(self, limit=5):
        """
        Return most frequently seen file paths.
        """

        counter = defaultdict(int)

        for _, _, path in self.events:
            counter[path] += 1

        return sorted(
            counter.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:limit]

    def burst_detected(self, threshold=100):
        """
        Simple burst detection rule:
        if total events exceed threshold in window.
        """

        return len(self.events) > threshold

    # ----------------------------------------------------
    # Helpers
    # ----------------------------------------------------

    def _parse_timestamp(self, ts):

        if isinstance(ts, datetime):
            return ts

        return datetime.strptime(
            ts,
            "%Y-%m-%d %H:%M:%S",
        )


# --------------------------------------------------------
# CLI demo
# --------------------------------------------------------

if __name__ == "__main__":

    from monitor.file_monitor import FileEvent

    tracker = EventTracker(window_seconds=60)

    print("Simulating events...\n")

    for i in range(120):

        event = FileEvent(
            event_type="modified",
            path=f"/tmp/file_{i}.txt",
            timestamp=datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        )

        tracker.add_event(event)

    print("Total events:", tracker.total_events())
    print("Rate/min:", tracker.event_rate_per_minute())
    print("Burst detected:", tracker.burst_detected())
    print("By type:", tracker.count_by_event_type())