"""
SmartSort AI
Safe Duplicate Cleanup Manager

Moves selected duplicate files into a SmartSort
Trash folder instead of permanently deleting them.

Supports undo/restore of the last cleanup.
"""

from pathlib import Path
from datetime import datetime
import shutil
import json


TRASH_FOLDER_NAME = ".smartsort_trash"


def get_trash_folder(folder_path):
    """
    Return the SmartSort Trash folder.
    """

    folder = Path(folder_path)

    trash_folder = folder / TRASH_FOLDER_NAME

    trash_folder.mkdir(
        exist_ok=True
    )

    return trash_folder


def create_unique_destination(
    destination
):
    """
    Create a unique destination path if a file
    with the same name already exists.
    """

    destination = Path(destination)

    if not destination.exists():
        return destination

    counter = 1

    while True:

        new_name = (
            f"{destination.stem}_"
            f"{counter}"
            f"{destination.suffix}"
        )

        new_path = (
            destination.parent /
            new_name
        )

        if not new_path.exists():
            return new_path

        counter += 1


def move_to_smart_trash(
    folder_path,
    files
):
    """
    Move selected files into SmartSort Trash.

    Returns:
        dictionary containing cleanup information.
    """

    folder = Path(folder_path)

    trash_folder = get_trash_folder(
        folder
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    session_folder = (
        trash_folder /
        timestamp
    )

    session_folder.mkdir(
        exist_ok=True
    )

    records = []

    for file in files:

        source = Path(file)

        if not source.exists():
            continue

        try:

            relative_path = source.relative_to(
                folder
            )

        except ValueError:

            relative_path = Path(
                source.name
            )

        destination = (
            session_folder /
            relative_path
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        destination = create_unique_destination(
            destination
        )

        try:

            shutil.move(
                str(source),
                str(destination)
            )

            records.append(
                {
                    "original": str(source),
                    "trash": str(destination)
                }
            )

        except (
            OSError,
            shutil.Error
        ):

            continue

    manifest_path = (
        session_folder /
        "manifest.json"
    )

    with open(
        manifest_path,
        "w",
        encoding="utf-8"
    ) as manifest:

        json.dump(
            records,
            manifest,
            indent=4
        )

    return {
        "session": str(session_folder),
        "records": records
    }


def undo_cleanup(
    cleanup_session
):
    """
    Restore files from the SmartSort Trash
    to their original locations.

    Returns:
        Number of restored files.
    """

    session_folder = Path(
        cleanup_session
    )

    manifest_path = (
        session_folder /
        "manifest.json"
    )

    if not manifest_path.exists():
        return 0

    try:

        with open(
            manifest_path,
            "r",
            encoding="utf-8"
        ) as manifest:

            records = json.load(
                manifest
            )

    except (
        OSError,
        json.JSONDecodeError
    ):

        return 0

    restored = 0

    for record in records:

        original = Path(
            record["original"]
        )

        trash_file = Path(
            record["trash"]
        )

        if not trash_file.exists():
            continue

        try:

            original.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            destination = (
                original
            )

            if destination.exists():

                destination = (
                    create_unique_destination(
                        destination
                    )
                )

            shutil.move(
                str(trash_file),
                str(destination)
            )

            restored += 1

        except (
            OSError,
            shutil.Error
        ):

            continue

    return restored