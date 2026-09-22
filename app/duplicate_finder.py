"""
SmartSort AI
Duplicate File Detection Engine

Uses SHA-256 hashes to identify files
with identical contents.
"""

from pathlib import Path
import hashlib


def calculate_file_hash(file_path, chunk_size=1024 * 1024):
    """
    Calculate the SHA-256 hash of a file.

    Files are read in chunks to avoid loading
    large files completely into memory.
    """

    sha256 = hashlib.sha256()

    try:

        with open(
            file_path,
            "rb"
        ) as file:

            while True:

                chunk = file.read(
                    chunk_size
                )

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()

    except (OSError, PermissionError):

        return None


def find_duplicates(folder_path):
    """
    Find duplicate files inside a folder.

    Returns:
        dictionary where the key is the file hash
        and the value is a list of duplicate files.
    """

    folder = Path(folder_path)

    if not folder.exists():
        return {}

    if not folder.is_dir():
        return {}

    # ------------------------------------------
    # Group files by size first
    # ------------------------------------------

    size_groups = {}

    for file in folder.rglob("*"):

        if not file.is_file():
            continue

        try:

            file_size = file.stat().st_size

        except OSError:

            continue

        size_groups.setdefault(
            file_size,
            []
        ).append(file)

    # ------------------------------------------
    # Hash only files with the same size
    # ------------------------------------------

    hash_groups = {}

    for file_size, files in size_groups.items():

        # A unique file size cannot produce
        # duplicates, so skip it.
        if len(files) < 2:
            continue

        for file in files:

            file_hash = calculate_file_hash(
                file
            )

            if file_hash is None:
                continue

            hash_groups.setdefault(
                file_hash,
                []
            ).append(file)

    # ------------------------------------------
    # Keep only actual duplicate groups
    # ------------------------------------------

    duplicates = {
        file_hash: files
        for file_hash, files
        in hash_groups.items()
        if len(files) > 1
    }

    return duplicates


def get_duplicate_statistics(duplicates):
    """
    Calculate duplicate statistics.

    Returns:
        duplicate_groups,
        duplicate_files,
        potential_space
    """

    duplicate_groups = len(
        duplicates
    )

    duplicate_files = 0
    potential_space = 0

    for files in duplicates.values():

        # Keep one copy and consider the
        # remaining files as duplicates.
        duplicate_files += len(files) - 1

        try:

            file_size = files[0].stat().st_size

            potential_space += (
                file_size *
                (len(files) - 1)
            )

        except OSError:

            pass

    return (
        duplicate_groups,
        duplicate_files,
        potential_space
    )