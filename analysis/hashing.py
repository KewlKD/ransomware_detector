from pathlib import Path
import hashlib


SUPPORTED_ALGORITHMS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}


# ----------------------------------------------------
# Generic hashing
# ----------------------------------------------------

def hash_bytes(data: bytes, algorithm="sha256"):
    """
    Hash a bytes object.

    Returns
    -------
    str
        Hex digest.
    """

    algorithm = algorithm.lower()

    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    hasher = SUPPORTED_ALGORITHMS[algorithm]()
    hasher.update(data)

    return hasher.hexdigest()


# ----------------------------------------------------
# File hashing
# ----------------------------------------------------

def hash_file(path, algorithm="sha256", chunk_size=65536):
    """
    Hash a file.

    Parameters
    ----------
    path : str | Path
    algorithm : str
    chunk_size : int

    Returns
    -------
    str
    """

    algorithm = algorithm.lower()

    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    hasher = SUPPORTED_ALGORITHMS[algorithm]()

    path = Path(path)

    with path.open("rb") as file:

        while True:

            chunk = file.read(chunk_size)

            if not chunk:
                break

            hasher.update(chunk)

    return hasher.hexdigest()


# ----------------------------------------------------
# Multiple hashes
# ----------------------------------------------------

def hash_file_all(path):
    """
    Calculate several hashes in one pass.

    Returns
    -------
    dict
    """

    path = Path(path)

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()

    with path.open("rb") as file:

        while True:

            chunk = file.read(65536)

            if not chunk:
                break

            md5.update(chunk)
            sha1.update(chunk)
            sha256.update(chunk)
            sha512.update(chunk)

    return {
        "md5": md5.hexdigest(),
        "sha1": sha1.hexdigest(),
        "sha256": sha256.hexdigest(),
        "sha512": sha512.hexdigest(),
    }


# ----------------------------------------------------
# Compare files
# ----------------------------------------------------

def files_match(file1, file2, algorithm="sha256"):
    """
    Compare two files using a hash.

    Returns
    -------
    bool
    """

    return (
        hash_file(file1, algorithm)
        ==
        hash_file(file2, algorithm)
    )


# ----------------------------------------------------
# Verify known hash
# ----------------------------------------------------

def verify_hash(path, expected_hash, algorithm="sha256"):
    """
    Verify a file matches an expected hash.

    Returns
    -------
    bool
    """

    return (
        hash_file(path, algorithm).lower()
        ==
        expected_hash.lower()
    )


# ----------------------------------------------------
# Directory manifest
# ----------------------------------------------------

def build_manifest(directory, algorithm="sha256"):
    """
    Build a hash manifest for every file
    in a directory.

    Returns
    -------
    dict
    """

    directory = Path(directory)

    manifest = {}

    for file in directory.rglob("*"):

        if file.is_file():

            manifest[str(file)] = hash_file(
                file,
                algorithm,
            )

    return manifest


# ----------------------------------------------------
# CLI
# ----------------------------------------------------

if __name__ == "__main__":

    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="File hashing utility"
    )

    parser.add_argument("file")

    parser.add_argument(
        "--algorithm",
        default="sha256",
        choices=list(SUPPORTED_ALGORITHMS.keys()),
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Calculate all supported hashes.",
    )

    args = parser.parse_args()

    if args.all:

        print(
            json.dumps(
                hash_file_all(args.file),
                indent=4,
            )
        )

    else:

        print(
            hash_file(
                args.file,
                args.algorithm,
            )
        )