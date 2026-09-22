from app.duplicate_finder import (
    find_duplicates,
    get_duplicate_statistics
)


folder = input(
    "Enter folder path to scan for duplicates: "
).strip()


duplicates = find_duplicates(folder)


groups, files, space = (
    get_duplicate_statistics(
        duplicates
    )
)


print("\n===================================")
print("       DUPLICATE FILE REPORT")
print("===================================")

print(
    f"\nDuplicate Groups : {groups}"
)

print(
    f"Duplicate Files  : {files}"
)

print(
    f"Potential Space  : "
    f"{space / (1024 * 1024):.2f} MB"
)


if duplicates:

    print(
        "\n========== DUPLICATE GROUPS ==========\n"
    )

    group_number = 1

    for file_hash, duplicate_files in (
        duplicates.items()
    ):

        print(
            f"Group {group_number}"
        )

        print(
            f"Hash: {file_hash}"
        )

        for file in duplicate_files:

            print(
                f"   └── {file}"
            )

        print()

        group_number += 1

else:

    print(
        "\n✅ No duplicate files found."
    )

print(
    "==================================="
)