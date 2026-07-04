from datetime import datetime, timedelta
from collections import deque


def now():
    """
    Return the current local time.
    """
    return datetime.now()


def utc_now():
    """
    Return the current UTC time.
    """
    return datetime.utcnow()


def format_timestamp(timestamp=None, fmt="%Y-%m-%d %H:%M:%S"):
    """
    Format a datetime object as a string.
    """

    if timestamp is None:
        timestamp = now()

    return timestamp.strftime(fmt)


def parse_timestamp(text, fmt="%Y-%m-%d %H:%M:%S"):
    """
    Parse a timestamp string into a datetime object.
    """

    return datetime.strptime(text, fmt)


def seconds_between(start, end):
    """
    Return the number of seconds between two datetime objects.
    """

    return (end - start).total_seconds()


def minutes_between(start, end):
    """
    Return the number of minutes between two datetime objects.
    """

    return seconds_between(start, end) / 60


def hours_between(start, end):
    """
    Return the number of hours between two datetime objects.
    """

    return seconds_between(start, end) / 3600


def add_seconds(timestamp, seconds):
    """
    Add seconds to a timestamp.
    """

    return timestamp + timedelta(seconds=seconds)


def add_minutes(timestamp, minutes):
    """
    Add minutes to a timestamp.
    """

    return timestamp + timedelta(minutes=minutes)


def add_hours(timestamp, hours):
    """
    Add hours to a timestamp.
    """

    return timestamp + timedelta(hours=hours)


class SlidingTimeWindow:
    """
    Maintain timestamps inside a rolling time window.

    Useful for:
        - rate limiting
        - counting recent events
        - simple burst detection
    """

    def __init__(self, window_seconds=60):
        self.window = timedelta(seconds=window_seconds)
        self.events = deque()

    def add_event(self, timestamp=None):
        """
        Add a timestamp to the window.
        """

        if timestamp is None:
            timestamp = now()

        self.events.append(timestamp)

        self._cleanup(timestamp)

    def count(self):
        """
        Return number of timestamps currently inside the window.
        """

        if self.events:
            self._cleanup(self.events[-1])

        return len(self.events)

    def clear(self):
        """
        Remove all stored timestamps.
        """

        self.events.clear()

    def _cleanup(self, current_time):
        """
        Remove timestamps outside the window.
        """

        while self.events:

            oldest = self.events[0]

            if current_time - oldest > self.window:
                self.events.popleft()
            else:
                break


if __name__ == "__main__":

    window = SlidingTimeWindow(window_seconds=10)

    print("Adding events...")

    window.add_event()

    window.add_event()

    window.add_event()

    print("Current event count:", window.count())