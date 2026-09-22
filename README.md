# SmartSort AI

> Intelligent Desktop File Organizer & Duplicate Detector

SmartSort AI is a Python-based desktop application that helps users organize files, identify duplicate files, review duplicates safely, and restore files when needed.

The project is designed with a safety-first approach: duplicate cleanup moves selected files to a local **SmartSort Trash** folder instead of permanently deleting them, with support for undo/restore.

---

## ✨ Features

### 📂 Intelligent File Organization
- Scans files in a selected folder.
- Classifies files based on their file extensions.
- Organizes files into categories such as:
  - Documents
  - Images
  - Videos
  - Audio
  - Code
  - Spreadsheets
  - Presentations
  - Other

### 🔍 Duplicate File Detection
- Recursively scans folders for duplicate files.
- Uses **SHA-256 hashing** to compare file contents.
- Groups files with identical content.
- Calculates potential storage savings from duplicate removal.

### 🛡️ Safe Duplicate Cleanup
- Provides a duplicate review window before cleanup.
- Allows users to select which duplicate copies should be removed.
- Moves selected files to `.smartsort_trash/` instead of permanently deleting them.
- Maintains a cleanup manifest for restoration.

### ↩️ Undo / Restore
- Restores files from the latest SmartSort cleanup session.
- Recreates required directories automatically.
- Protects existing files by creating a unique filename when necessary.

### 🖥️ Desktop GUI
Built with **CustomTkinter**, featuring:
- Folder selection
- Scan Folder
- Organize Files
- Find Duplicates
- Duplicate review
- Undo cleanup
- Dashboard statistics
- Progress indicator
- Status messages

---

## 🖥️ Application Dashboard

The SmartSort AI dashboard provides an overview of:

| Metric | Description |
|---|---|
| Files | Number of files detected |
| Categories | Number of file categories |
| Storage | Total storage used by scanned files |
| Duplicates | Number of duplicate files identified |
| Status | Current operation status |

---

## 🧠 How It Works

### File Organization

```text
Selected Folder
      │
      ▼
Scan Files
      │
      ▼
Read File Extensions
      │
      ▼
Classify Files
      │
      ▼
Create Category Folders
      │
      ▼
Move Files
```

### Duplicate Detection

```text
Selected Folder
      │
      ▼
Recursive File Scan
      │
      ▼
Group Files by Size
      │
      ▼
Calculate SHA-256 Hash
      │
      ▼
Group Identical Hashes
      │
      ▼
Display Duplicate Groups
```

### Safe Cleanup

```text
Duplicate Review
      │
      ▼
User Selects Files
      │
      ▼
Move to .smartsort_trash/
      │
      ▼
Create manifest.json
      │
      ▼
Files Can Be Restored
```

---

## 📁 Project Structure

```text
SmartSort-AI/
│
├── app/
│   ├── __init__.py
│   ├── classifier.py
│   ├── organizer.py
│   ├── duplicate_finder.py
│   ├── cleanup_manager.py
│   └── gui.py
│
├── assets/
│
├── logs/
│
├── screenshots/
│
├── tests/
│
├── DuplicateTest/
│   └── Duplicate detection test files
│
├── GUITest/
│   └── GUI demonstration files
│
├── TestFiles/
│   └── Sample files for organization testing
│
├── main.py
├── test_duplicates.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Technology Stack

- **Python 3**
- **CustomTkinter** — Modern desktop GUI
- **Tkinter** — GUI foundation
- **Pathlib** — File and directory handling
- **hashlib** — SHA-256 duplicate detection
- **shutil** — Safe file movement
- **JSON** — Cleanup session manifests
- **Git & GitHub** — Version control and project hosting

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/itzmemsd/SmartSort-AI.git
cd SmartSort-AI
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## ▶️ Running SmartSort AI

From the project directory:

```powershell
python main.py
```

The SmartSort AI desktop application will open.

---

## 🧪 Testing

The repository contains sample files for testing different SmartSort functions.

### Duplicate detection test

Run:

```powershell
python test_duplicates.py
```

The `DuplicateTest/` directory contains files that can be used to test duplicate detection.

The `TestFiles/` directory contains sample files representing different categories.

---

## 🔐 Safety Design

SmartSort AI is designed to avoid irreversible duplicate deletion.

Instead of directly deleting selected files:

```text
User selects duplicate
        ↓
SmartSort moves file
        ↓
.smartsort_trash/
        ↓
manifest.json records original location
        ↓
Undo can restore the file
```

This provides an additional recovery layer during duplicate cleanup.

> **Important:** Users should still maintain normal backups of important data. SmartSort AI is a file-management utility and should not be considered a replacement for a backup system.

---

## 📊 Duplicate Detection Method

SmartSort AI uses a two-stage process to reduce unnecessary hashing:

### Stage 1 — File Size Grouping

Files are first grouped according to their file size.

Files with different sizes cannot have identical complete contents, so they do not need to be hashed against each other.

### Stage 2 — SHA-256 Hashing

Files with the same size are processed using SHA-256.

Conceptually:

```text
File A → SHA-256 → Hash A
File B → SHA-256 → Hash B
File C → SHA-256 → Hash A
```

If File A and File C produce the same SHA-256 hash, they are grouped as duplicates.

---

## 🎯 Current Capabilities

| Capability | Status |
|---|---|
| Desktop GUI | ✅ |
| File classification | ✅ |
| File organization | ✅ |
| Recursive duplicate scanning | ✅ |
| SHA-256 duplicate detection | ✅ |
| Duplicate review | ✅ |
| Safe cleanup | ✅ |
| Cleanup manifest | ✅ |
| Undo / restore | ✅ |
| Dashboard statistics | ✅ |
| Progress indicator | ✅ |
| Automated AI content classification | 🚧 Planned |
| Advanced storage analytics | 🚧 Planned |
| Intelligent cleanup recommendations | 🚧 Planned |

---

## 🗺️ Roadmap

Future versions may include:

- [ ] AI-based semantic file classification
- [ ] Content-aware document classification
- [ ] Image and media metadata analysis
- [ ] Advanced storage analytics
- [ ] Large-file detection
- [ ] Duplicate similarity analysis
- [ ] Smart cleanup recommendations
- [ ] Scheduled organization
- [ ] Configurable category rules
- [ ] Custom file-extension rules
- [ ] Search and filtering
- [ ] Dark/light theme controls
- [ ] Exportable storage reports
- [ ] Improved test coverage
- [ ] Application packaging for Windows
- [ ] Installer creation

---

## 💡 Project Vision

SmartSort AI aims to evolve from a rule-based file organizer into an intelligent personal file-management assistant.

The long-term goal is to combine:

```text
File Organization
        +
Duplicate Detection
        +
Storage Analytics
        +
AI Classification
        +
Safe Automation
```

into a single desktop productivity application.

---

## 👨‍💻 Author

**Sasidharan Murugan**

GitHub: [@itzmemsd](https://github.com/itzmemsd)

---

## 📄 License

This project currently does not include a license file.

A license can be added in a future release depending on how the project will be distributed and reused.

---

## ⭐ Contributing

Suggestions, bug reports, improvements, and feature ideas are welcome.

If you find an issue, please open a GitHub Issue with:

1. A clear description of the problem.
2. Steps to reproduce it.
3. Expected behavior.
4. Actual behavior.
5. Relevant error messages or screenshots.

---

## 📌 Project Status

**Current version:** Initial Development Release

SmartSort AI is actively being developed. Features and architecture may change as the project evolves.
