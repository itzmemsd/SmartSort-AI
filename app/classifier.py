from pathlib import Path


FILE_CATEGORIES = {
    "Documents": {
        ".pdf",
        ".doc",
        ".docx",
        ".txt",
        ".rtf",
        ".odt",
    },

    "Images": {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp",
        ".svg",
    },

    "Videos": {
        ".mp4",
        ".avi",
        ".mkv",
        ".mov",
        ".wmv",
        ".flv",
    },

    "Audio": {
        ".mp3",
        ".wav",
        ".aac",
        ".flac",
        ".ogg",
        ".m4a",
    },

    "Spreadsheets": {
        ".xls",
        ".xlsx",
        ".csv",
        ".ods",
    },

    "Presentations": {
        ".ppt",
        ".pptx",
        ".odp",
    },

    "Archives": {
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz",
    },

    "Code": {
        ".py",
        ".js",
        ".html",
        ".css",
        ".java",
        ".cpp",
        ".c",
        ".php",
        ".sql",
    },
}


def classify_file(file_path):
    """
    Identify the category of a file based on its extension.
    """

    extension = Path(file_path).suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Other"