"""
main.py

Entry point for the educational filesystem monitoring project.
"""

from pathlib import Path
import signal
import sys

from config import Config
from monitor.file_monitor import FileMonitor
from utils.logger import setup_logger


class Application:
    def __init__(self):
        self.config = Config()
        self.logger = setup_logger(self.config.LOG_LEVEL)

        self.monitor = FileMonitor(
            directory=self.config.MONITOR_DIRECTORY,
            callback=self.handle_event,
            logger=self.logger,
        )

    def handle_event(self, event):
        """
        Callback invoked whenever the monitor reports an event.

        The event is expected to expose:
            event.event_type
            event.path
            event.timestamp
        """

        self.logger.info(
            "[%s] %s (%s)",
            event.event_type,
            event.path,
            event.timestamp,
        )

    def run(self):
        directory = Path(self.config.MONITOR_DIRECTORY)

        if not directory.exists():
            self.logger.error(
                "Directory does not exist: %s",
                directory,
            )
            return

        self.logger.info("Monitoring: %s", directory)

        self.monitor.start()

        self.logger.info("Press Ctrl+C to stop.")

        try:
            self.monitor.join()

        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        self.logger.info("Stopping monitor...")

        self.monitor.stop()

        self.logger.info("Goodbye.")


def register_signal_handlers(app):

    def handler(signum, frame):
        app.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)


def main():

    app = Application()

    register_signal_handlers(app)

    app.run()


if __name__ == "__main__":
    main()