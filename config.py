from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """
    Application-wide configuration settings.
    """

    # ----------------------------------------------------
    # Paths
    # ----------------------------------------------------

    MONITOR_DIRECTORY: str = "./watched"
    LOG_DIRECTORY: str = "./logs"
    ALERT_LOG_FILE: str = "alerts.json"

    # ----------------------------------------------------
    # Logging
    # ----------------------------------------------------

    LOG_LEVEL: str = "INFO"

    # ----------------------------------------------------
    # Event tracking
    # ----------------------------------------------------

    WINDOW_SECONDS: int = 60
    MAX_EVENTS_PER_MINUTE: int = 250

    # ----------------------------------------------------
    # Heuristics thresholds
    # ----------------------------------------------------

    MAX_AVERAGE_ENTROPY: float = 7.5
    MAX_LARGE_FILE_MB: float = 100
    MAX_UNIQUE_EXTENSIONS: int = 50

    # ----------------------------------------------------
    # Behavior flags
    # ----------------------------------------------------

    ENABLE_ALERTING: bool = True
    ENABLE_TRACKING: bool = True

    # ----------------------------------------------------
    # Derived paths
    # ----------------------------------------------------

    def monitor_path(self) -> Path:
        return Path(self.MONITOR_DIRECTORY)

    def log_path(self) -> Path:
        return Path(self.LOG_DIRECTORY)

    def alert_file_path(self) -> Path:
        return self.log_path() / self.ALERT_LOG_FILE


# Singleton-style access (simple and common in small tools)

CONFIG = Config()


# --------------------------------------------------------
# Helper for CLI overrides (optional expansion point)
# --------------------------------------------------------

def load_config(overrides: dict | None = None) -> Config:
    """
    Create a config instance with optional overrides.

    Example:
        load_config({"WINDOW_SECONDS": 120})
    """

    cfg = Config()

    if overrides:

        for key, value in overrides.items():

            if hasattr(cfg, key):
                setattr(cfg, key, value)

    return cfg