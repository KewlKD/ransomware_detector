from pathlib import Path
from collections import Counter
import math


# --------------------------------------------------------
# Core entropy calculation
# --------------------------------------------------------

def shannon_entropy(data: bytes) -> float:
    """
    Calculate Shannon entropy for bytes.

    Parameters
    ----------
    data : bytes

    Returns
    -------
    float
    """

    if not data:
        return 0.0

    counts = Counter(data)
    length = len(data)

    entropy = 0.0

    for count in counts.values():

        probability = count / length

        entropy -= probability * math.log2(probability)

    return entropy


# --------------------------------------------------------
# File entropy
# --------------------------------------------------------

def file_entropy(path):
    """
    Calculate entropy for an entire file.

    Parameters
    ----------
    path : str | Path

    Returns
    -------
    float
    """

    path = Path(path)

    with path.open("rb") as file:
        data = file.read()

    return shannon_entropy(data)


# --------------------------------------------------------
# String entropy
# --------------------------------------------------------

def string_entropy(text: str) -> float:
    """
    Calculate entropy for a text string.
    """

    return shannon_entropy(text.encode("utf-8"))


# --------------------------------------------------------
# Chunk entropy
# --------------------------------------------------------

def chunk_entropy(path, chunk_size=4096):
    """
    Calculate entropy for each chunk of a file.

    Returns
    -------
    list[float]
    """

    entropies = []

    path = Path(path)

    with path.open("rb") as file:

        while True:

            chunk = file.read(chunk_size)

            if not chunk:
                break

            entropies.append(
                shannon_entropy(chunk)
            )

    return entropies


# --------------------------------------------------------
# Average entropy
# --------------------------------------------------------

def average_chunk_entropy(path, chunk_size=4096):
    """
    Average entropy across all chunks.
    """

    values = chunk_entropy(path, chunk_size)

    if not values:
        return 0.0

    return sum(values) / len(values)


# --------------------------------------------------------
# Classification
# --------------------------------------------------------

def classify_entropy(entropy):
    """
    Human-readable interpretation.

    NOTE:
    These are only rough educational ranges.
    """

    if entropy < 3:
        return "Low"

    if entropy < 6:
        return "Moderate"

    if entropy < 7.5:
        return "High"

    return "Very High"


# --------------------------------------------------------
# Pretty report
# --------------------------------------------------------

def entropy_report(path):
    """
    Generate a dictionary summarizing file entropy.
    """

    path = Path(path)

    entropy = file_entropy(path)

    return {
        "file": path.name,
        "size_bytes": path.stat().st_size,
        "entropy": round(entropy, 3),
        "classification": classify_entropy(entropy),
    }


# --------------------------------------------------------
# CLI
# --------------------------------------------------------

if __name__ == "__main__":

    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Calculate Shannon entropy for files."
    )

    parser.add_argument(
        "file",
        help="Path to file"
    )

    parser.add_argument(
        "--chunks",
        action="store_true",
        help="Display entropy per chunk"
    )

    args = parser.parse_args()

    report = entropy_report(args.file)

    print(json.dumps(report, indent=4))

    if args.chunks:

        print("\nChunk Entropies\n")

        for i, value in enumerate(chunk_entropy(args.file), start=1):

            print(
                f"Chunk {i:03d}: "
                f"{value:.3f}"
            )