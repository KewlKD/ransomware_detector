from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import time


# --------------------------------------------------------
# Event model
# --------------------------------------------------------

@dataclass
class FileEvent:
    event_type: str
    path: str
    timestamp: str


# --------------------------------------------------------
# Watchdog handler
# --------------------------------------------------------

class _Handler(FileSystemEventHandler):
    """
    Internal event handler that converts watchdog events
    into FileEvent objects.
    """

    def __init__(self, callback, logger=None):
        self.callback = callback
        self.logger = logger

    def _emit(self, event_type, path):

        event = FileEvent(
            event_type=event_type,
            path=str(path),
            timestamp=datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        )

        if self.logger:
            self.logger.debug(
                "Event: %s -> %s",
                event_type,
                path,
            )

        self.callback(event)

    def on_created(self, event):

        if not event.is_directory:
            self._emit("created", event.src_path)

    def on_modified(self, event):

        if not event.is_directory:
            self._emit("modified", event.src_path)

    def on_deleted(self, event):

        if not event.is_directory:
            self._emit("deleted", event.src_path)

    def on_moved(self, event):

        if not event.is_directory:
            self._emit(
                "moved",
                f"{event.src_path} -> {event.dest_path}",
            )


# --------------------------------------------------------
# Public monitor class
# --------------------------------------------------------

class FileMonitor:
    """
    Watches a directory for file system changes.
    """

    def __init__(self, directory, callback, logger=None):

        self.directory = Path(directory)
        self.callback = callback
        self.logger = logger

        self.observer = Observer()
        self.handler = _Handler(callback, logger)

        self._running = False

    def start(self):
        """
        Start monitoring.
        """

        self.directory.mkdir(parents=True, exist_ok=True)

        self.observer.schedule(
            self.handler,
            str(self.directory),
            recursive=True,
        )

        self.observer.start()

        self._running = True

        if self.logger:
            self.logger.info(
                "Started monitoring %s",
                self.directory,
            )

    def stop(self):
        """
        Stop monitoring.
        """

        if self._running:

            self.observer.stop()
            self.observer.join()

            self._running = False

            if self.logger:
                self.logger.info("Stopped monitoring")

    def join(self):
        """
        Keep thread alive while monitoring.
        """

        try:
            while self._running:
                time.sleep(0.5)

        except KeyboardInterrupt:
            self.stop()