from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Finding:
    """
    Represents a heuristic observation.
    """
    severity: str
    title: str
    description: str


class HeuristicEngine:
    """
    Evaluate metrics using configurable thresholds.
    """

    def __init__(self, config=None):

        default = {
            "max_events_per_minute": 250,
            "max_average_entropy": 7.5,
            "max_file_size_mb": 100,
            "max_unique_extensions": 50,
        }

        self.config = config or default

    def evaluate(self, metrics: Dict) -> List[Finding]:
        """
        Evaluate a metrics dictionary.

        Parameters
        ----------
        metrics : dict

        Example
        -------
        {
            "events_per_minute": 175,
            "average_entropy": 6.9,
            "largest_file_mb": 12,
            "unique_extensions": 8,
        }
        """

        findings = []

        findings.extend(self._check_event_rate(metrics))
        findings.extend(self._check_entropy(metrics))
        findings.extend(self._check_file_size(metrics))
        findings.extend(self._check_extensions(metrics))

        return findings

    def _check_event_rate(self, metrics):

        findings = []

        rate = metrics.get("events_per_minute", 0)

        if rate > self.config["max_events_per_minute"]:

            findings.append(
                Finding(
                    severity="WARNING",
                    title="High Event Rate",
                    description=(
                        f"Observed {rate} events per minute "
                        f"(threshold "
                        f"{self.config['max_events_per_minute']})."
                    ),
                )
            )

        return findings

    def _check_entropy(self, metrics):

        findings = []

        entropy = metrics.get("average_entropy")

        if entropy is None:
            return findings

        if entropy > self.config["max_average_entropy"]:

            findings.append(
                Finding(
                    severity="INFO",
                    title="High Average Entropy",
                    description=(
                        f"Average entropy "
                        f"{entropy:.2f} exceeds configured "
                        "threshold."
                    ),
                )
            )

        return findings

    def _check_file_size(self, metrics):

        findings = []

        size = metrics.get("largest_file_mb")

        if size is None:
            return findings

        if size > self.config["max_file_size_mb"]:

            findings.append(
                Finding(
                    severity="INFO",
                    title="Large File Observed",
                    description=(
                        f"Largest processed file "
                        f"{size:.2f} MB."
                    ),
                )
            )

        return findings

    def _check_extensions(self, metrics):

        findings = []

        count = metrics.get("unique_extensions", 0)

        if count > self.config["max_unique_extensions"]:

            findings.append(
                Finding(
                    severity="INFO",
                    title="Many File Types",
                    description=(
                        f"{count} unique file extensions "
                        "observed."
                    ),
                )
            )

        return findings


def summarize_findings(findings: List[Finding]) -> Dict:
    """
    Build a summary dictionary.
    """

    summary = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "total": len(findings),
    }

    for finding in findings:

        if finding.severity in summary:
            summary[finding.severity] += 1

    return summary


if __name__ == "__main__":

    sample_metrics = {
        "events_per_minute": 320,
        "average_entropy": 7.8,
        "largest_file_mb": 180,
        "unique_extensions": 61,
    }

    engine = HeuristicEngine()

    findings = engine.evaluate(sample_metrics)

    print("Findings\n")

    for finding in findings:

        print(
            f"[{finding.severity}] "
            f"{finding.title}"
        )

        print(f"  {finding.description}\n")

    print("Summary")
    print(summarize_findings(findings))