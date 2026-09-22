from pathlib import Path
import shutil

from app.classifier import classify_file


def get_unique_path(destination):
    """
    Return a unique file path if the destination already exists.
    """

    destination = Path(destination)

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = (
            f"{destination.stem}_{counter}"
            f"{destination.suffix}"
        )

        new_path = destination.parent / new_name

        if not new_path.exists():
            return new_path

        counter += 1


def organize_folder(folder_path):
    """
    Organize files into category folders.
    """

    folder = Path(folder_path)

    if not folder.exists():
        print("❌ Folder does not exist.")
        return

    if not folder.is_dir():
        print("❌ The selected path is not a folder.")
        return

    files = [
        file
        for file in folder.iterdir()
        if file.is_file()
    ]

    if not files:
        print("📂 No files found.")
        return

    moved_count = 0

    print("\n========================================")
    print("       SmartSort AI - Organizer")
    print("========================================\n")

    for file in files:

        category = classify_file(file)

        category_folder = folder / category

        category_folder.mkdir(
            exist_ok=True
        )

        destination = category_folder / file.name

        destination = get_unique_path(destination)

        try:
            shutil.move(
                str(file),
                str(destination)
            )

            print(
                f"✅ {file.name}"
                f" → {category}/"
                f"{destination.name}"
            )

            moved_count += 1

        except Exception as error:

            print(
                f"❌ Could not move "
                f"{file.name}: {error}"
            )

    print("\n========================================")
    print(f"Successfully organized: {moved_count} files")
    print("========================================")