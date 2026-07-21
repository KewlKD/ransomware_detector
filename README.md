# 🛡️ Ransomware Detector 

A defensive cybersecurity project written in Python that demonstrates how to monitor filesystem activity, track events, calculate file entropy, verify file integrity with hashes, and generate alerts.


# Features

- Monitor a directory for file activity
- Log file creation, modification, deletion, and rename events
- Track filesystem activity over time
- Calculate Shannon entropy of files
- Generate SHA-256, SHA-1, SHA-512, and MD5 hashes
- Evaluate metrics using configurable heuristics
- Generate informational, warning, and critical alerts
- JSON sample data for testing
- Unit tests using pytest
- Modular project architecture

---

# Project Structure

```text
ransomware-detector/
│
├── main.py
├── config.py
├── requirements.txt
├── README.md
│
├── watched/
│
├── logs/
│
├── data/
│   └── sample_logs.json
│
├── analysis/
│   ├── entropy.py
│   ├── hashing.py
│   └── heuristics.py
│
├── monitor/
│   ├── file_monitor.py
│   └── event_models.py
│
├── tracking/
│   └── event_tracker.py
│
├── alerting/
│   └── alerting.py
│
├── utils/
│   ├── logger.py
│   └── time_utils.py
│
└── tests/
    ├── test_entropy.py
    ├── test_hashing.py
    ├── test_monitor.py
    
```

---

# Requirements

- Python 3.11 or newer
- pip

---

# Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ransomware-detector.git
```

Enter the project directory:

```bash
cd ransomware-detector
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Requirements.txt

```text
watchdog>=3.0.0
pytest>=8.0.0
```

---

# Running the Application

Start the application:

```bash
python main.py
```

Example output:

```text
2026-07-04 15:00:00 | INFO | Monitoring: ./watched
Press Ctrl+C to stop.
```

---

# Testing

Run all unit tests:

```bash
pytest
```

Or:

```bash
pytest -q
```

---

# Example Workflow

1. Start the application

```bash
python main.py
```

2. Create a file

```bash
echo "Hello World" > watched/test.txt
```

3. Modify the file

```bash
echo "More text" >> watched/test.txt
```

4. Delete the file

```bash
rm watched/test.txt
```

The application logs each event.

---

# Configuration

Configuration values are stored in:

```
config.py
```

Examples:

```python
MONITOR_DIRECTORY = "./watched"

WINDOW_SECONDS = 60

MAX_EVENTS_PER_MINUTE = 250

LOG_LEVEL = "INFO"
```

---

# Modules

## monitor/

Responsible for filesystem monitoring using the watchdog library.

---

## tracking/

Tracks events over time and calculates event rates.

---

## analysis/

Contains reusable analysis modules:

- Shannon entropy
- File hashing
- Heuristic evaluation

---

## alerting/

Generates alerts and stores alert history.

---

## utils/

Contains helper modules including:

- Logging
- Time utilities

---

## tests/

Contains pytest unit tests.

---

# Technologies Used

- Python
- Watchdog
- Pytest
- Dataclasses
- Pathlib
- Logging
- Hashlib
- JSON


---

# License

This project is licensed under the MIT License.

---

# Disclaimer

This project is intended solely for educational purposes to demonstrate defensive cybersecurity concepts such as file monitoring, logging, integrity verification, and event analysis. It does **not** detect, prevent, or respond to ransomware attacks and should not be used as a production security solution.
