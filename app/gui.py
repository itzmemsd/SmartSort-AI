"""
SmartSort AI
Intelligent File Organizer
Duplicate Detector
Safe Duplicate Review
Undo Support
"""

import customtkinter as ctk

from tkinter import (
    filedialog,
    messagebox
)

from pathlib import Path

from app.classifier import classify_file

from app.organizer import organize_folder

from app.duplicate_finder import (
    find_duplicates,
    get_duplicate_statistics
)

from app.cleanup_manager import (
    move_to_smart_trash,
    undo_cleanup
)


class SmartSortApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        # ======================================
        # WINDOW
        # ======================================

        self.title(
            "SmartSort AI"
        )

        self.geometry(
            "1150x800"
        )

        self.minsize(
            1000,
            700
        )

        ctk.set_appearance_mode(
            "dark"
        )

        ctk.set_default_color_theme(
            "blue"
        )

        # ======================================
        # DATA
        # ======================================

        self.selected_folder = None

        self.total_files = 0

        self.total_size = 0

        self.category_count = {}

        self.duplicate_groups = 0

        self.duplicate_files = 0

        self.potential_space = 0

        self.current_duplicates = {}

        self.last_cleanup_session = None

        # ======================================
        # GUI
        # ======================================

        self.create_interface()

    # ==========================================
    # CREATE INTERFACE
    # ==========================================

    def create_interface(self):

        # --------------------------------------
        # HEADER
        # --------------------------------------

        self.header = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        self.header.pack(
            fill="x"
        )

        self.title_label = ctk.CTkLabel(
            self.header,
            text="🧹 SmartSort AI",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        )

        self.title_label.pack(
            pady=(18, 2)
        )

        self.subtitle_label = ctk.CTkLabel(
            self.header,
            text=(
                "Intelligent File Organizer "
                "& Duplicate Detector"
            ),
            font=ctk.CTkFont(
                size=15
            )
        )

        self.subtitle_label.pack(
            pady=(0, 18)
        )

        # --------------------------------------
        # MAIN
        # --------------------------------------

        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        # --------------------------------------
        # FOLDER
        # --------------------------------------

        self.folder_label = ctk.CTkLabel(
            self.main_frame,
            text="📁 Select Folder",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.folder_label.pack(
            anchor="w",
            padx=25,
            pady=(18, 8)
        )

        self.folder_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.folder_frame.pack(
            fill="x",
            padx=25
        )

        self.folder_entry = ctk.CTkEntry(
            self.folder_frame,
            placeholder_text="Choose a folder..."
        )

        self.folder_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        self.browse_button = ctk.CTkButton(
            self.folder_frame,
            text="Browse",
            width=120,
            command=self.browse_folder
        )

        self.browse_button.pack(
            side="right"
        )

        # --------------------------------------
        # DASHBOARD
        # --------------------------------------

        self.dashboard_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.dashboard_frame.pack(
            fill="x",
            padx=15,
            pady=18
        )

        for column in range(5):

            self.dashboard_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.files_card = self.create_card(
            self.dashboard_frame,
            "📄",
            "Files",
            "0",
            0
        )

        self.categories_card = self.create_card(
            self.dashboard_frame,
            "📂",
            "Categories",
            "0",
            1
        )

        self.size_card = self.create_card(
            self.dashboard_frame,
            "💾",
            "Storage",
            "0 B",
            2
        )

        self.duplicates_card = self.create_card(
            self.dashboard_frame,
            "🔁",
            "Duplicates",
            "0",
            3
        )

        self.status_card = self.create_card(
            self.dashboard_frame,
            "🟢",
            "Status",
            "Ready",
            4
        )

        # --------------------------------------
        # BUTTONS
        # --------------------------------------

        self.button_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.button_frame.pack(
            pady=3
        )

        self.scan_button = ctk.CTkButton(
            self.button_frame,
            text="🔍 Scan",
            width=150,
            height=42,
            command=self.scan_folder
        )

        self.scan_button.pack(
            side="left",
            padx=4
        )

        self.organize_button = ctk.CTkButton(
            self.button_frame,
            text="⚡ Organize",
            width=150,
            height=42,
            command=self.organize_files
        )

        self.organize_button.pack(
            side="left",
            padx=4
        )

        self.duplicate_button = ctk.CTkButton(
            self.button_frame,
            text="🔎 Duplicates",
            width=150,
            height=42,
            command=self.scan_duplicates
        )

        self.duplicate_button.pack(
            side="left",
            padx=4
        )

        self.review_button = ctk.CTkButton(
            self.button_frame,
            text="🛡 Review",
            width=150,
            height=42,
            command=self.review_duplicates
        )

        self.review_button.pack(
            side="left",
            padx=4
        )

        self.undo_button = ctk.CTkButton(
            self.button_frame,
            text="↩ Undo",
            width=150,
            height=42,
            command=self.undo_last_cleanup
        )

        self.undo_button.pack(
            side="left",
            padx=4
        )

        # --------------------------------------
        # PROGRESS
        # --------------------------------------

        self.progress = ctk.CTkProgressBar(
            self.main_frame
        )

        self.progress.pack(
            fill="x",
            padx=25,
            pady=(15, 4)
        )

        self.progress.set(0)

        self.progress_label = ctk.CTkLabel(
            self.main_frame,
            text="Ready"
        )

        self.progress_label.pack(
            pady=(0, 8)
        )

        # --------------------------------------
        # RESULTS
        # --------------------------------------

        self.results_label = ctk.CTkLabel(
            self.main_frame,
            text="📊 Results",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.results_label.pack(
            anchor="w",
            padx=25,
            pady=(3, 8)
        )

        self.results_box = ctk.CTkTextbox(
            self.main_frame,
            height=220,
            font=ctk.CTkFont(
                size=13
            )
        )

        self.results_box.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 18)
        )

        self.results_box.insert(
            "end",
            "Welcome to SmartSort AI!\n\n"
            "Select a folder and choose an action.\n\n"
            "🔍 Scan       Analyze files\n"
            "⚡ Organize   Sort files\n"
            "🔎 Duplicates Find duplicates\n"
            "🛡 Review     Review duplicates safely\n"
            "↩ Undo       Restore last cleanup\n"
        )

    # ==========================================
    # CARD
    # ==========================================

    def create_card(
        self,
        parent,
        icon,
        title,
        value,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            corner_radius=12
        )

        card.grid(
            row=0,
            column=column,
            padx=4,
            sticky="nsew"
        )

        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(
                size=20
            )
        )

        icon_label.pack(
            pady=(10, 1)
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=11
            )
        )

        title_label.pack()

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        value_label.pack(
            pady=(2, 10)
        )

        return value_label

    # ==========================================
    # BROWSE
    # ==========================================

    def browse_folder(self):

        folder = filedialog.askdirectory(
            title="Select Folder"
        )

        if not folder:
            return

        self.selected_folder = folder

        self.folder_entry.delete(
            0,
            "end"
        )

        self.folder_entry.insert(
            0,
            folder
        )

        self.reset_statistics()

        self.results_box.delete(
            "1.0",
            "end"
        )

        self.results_box.insert(
            "end",
            "Folder selected successfully.\n\n"
            "Choose an action."
        )

        self.progress.set(0)

        self.progress_label.configure(
            text="Ready"
        )

        self.update_status(
            "Folder Selected"
        )

    # ==========================================
    # RESET
    # ==========================================

    def reset_statistics(self):

        self.total_files = 0

        self.total_size = 0

        self.category_count = {}

        self.duplicate_groups = 0

        self.duplicate_files = 0

        self.potential_space = 0

        self.current_duplicates = {}

        self.update_dashboard()

    # ==========================================
    # VALIDATE
    # ==========================================

    def validate_folder(
        self,
        folder
    ):

        if not folder:

            messagebox.showwarning(
                "No Folder",
                "Please select a folder first."
            )

            return False

        path = Path(folder)

        if not path.exists():

            messagebox.showerror(
                "Invalid Folder",
                "The selected folder does not exist."
            )

            return False

        if not path.is_dir():

            messagebox.showerror(
                "Invalid Folder",
                "The selected path is not a folder."
            )

            return False

        return True

    # ==========================================
    # SCAN
    # ==========================================

    def scan_folder(self):

        folder = self.folder_entry.get().strip()

        if not self.validate_folder(folder):
            return

        path = Path(folder)

        files = [
            file
            for file in path.iterdir()
            if file.is_file()
        ]

        self.category_count = {}

        self.total_files = len(files)

        self.total_size = 0

        self.results_box.delete(
            "1.0",
            "end"
        )

        if not files:

            self.results_box.insert(
                "end",
                "📂 No files found."
            )

            self.update_dashboard()

            self.update_status(
                "No Files"
            )

            return

        self.results_box.insert(
            "end",
            "========== FILE ANALYSIS ==========\n\n"
        )

        for index, file in enumerate(
            files,
            start=1
        ):

            category = classify_file(
                file
            )

            self.category_count[
                category
            ] = (
                self.category_count.get(
                    category,
                    0
                ) + 1
            )

            try:

                self.total_size += (
                    file.stat().st_size
                )

            except OSError:

                pass

            self.results_box.insert(
                "end",
                f"{file.name:<35} → "
                f"{category}\n"
            )

            self.progress.set(
                index / len(files)
            )

            self.progress_label.configure(
                text=(
                    f"Scanning {index} "
                    f"of {len(files)}"
                )
            )

            self.update()

        self.results_box.insert(
            "end",
            "\n========== SUMMARY ==========\n\n"
        )

        for category, count in sorted(
            self.category_count.items()
        ):

            self.results_box.insert(
                "end",
                f"{category:<20} : "
                f"{count}\n"
            )

        self.results_box.insert(
            "end",
            "\nTotal Files : "
            f"{self.total_files}\n"
        )

        self.results_box.insert(
            "end",
            "Total Size  : "
            f"{self.format_size(self.total_size)}\n"
        )

        self.update_dashboard()

        self.progress.set(1)

        self.progress_label.configure(
            text="Scan complete — 100%"
        )

        self.update_status(
            "Scan Complete"
        )

    # ==========================================
    # ORGANIZE
    # ==========================================

    def organize_files(self):

        folder = self.folder_entry.get().strip()

        if not self.validate_folder(folder):
            return

        path = Path(folder)

        files = [
            file
            for file in path.iterdir()
            if file.is_file()
        ]

        if not files:

            messagebox.showinfo(
                "Nothing to Organize",
                "No files found."
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Organization",
            f"{len(files)} files will be "
            "organized into category folders.\n\n"
            "Continue?"
        )

        if not confirm:
            return

        self.total_files = len(files)

        self.total_size = 0

        self.category_count = {}

        for file in files:

            category = classify_file(
                file
            )

            self.category_count[
                category
            ] = (
                self.category_count.get(
                    category,
                    0
                ) + 1
            )

            try:

                self.total_size += (
                    file.stat().st_size
                )

            except OSError:

                pass

        self.progress.set(0)

        self.update_status(
            "Organizing..."
        )

        try:

            organize_folder(
                folder
            )

        except Exception as error:

            messagebox.showerror(
                "Organization Error",
                str(error)
            )

            self.update_status(
                "Organization Failed"
            )

            return

        self.update_dashboard()

        self.results_box.delete(
            "1.0",
            "end"
        )

        self.results_box.insert(
            "end",
            "========== ORGANIZATION ==========\n\n"
        )

        self.results_box.insert(
            "end",
            "✅ Organization completed.\n\n"
        )

        for category, count in sorted(
            self.category_count.items()
        ):

            self.results_box.insert(
                "end",
                f"📂 {category:<20} "
                f"{count} files\n"
            )

        self.progress.set(1)

        self.progress_label.configure(
            text="Organization complete — 100%"
        )

        self.update_status(
            "Organization Complete"
        )

        messagebox.showinfo(
            "Complete",
            f"Successfully organized "
            f"{len(files)} files."
        )

    # ==========================================
    # DUPLICATE SCAN
    # ==========================================

    def scan_duplicates(self):

        folder = self.folder_entry.get().strip()

        if not self.validate_folder(folder):
            return

        self.results_box.delete(
            "1.0",
            "end"
        )

        self.results_box.insert(
            "end",
            "========== DUPLICATE SCAN ==========\n\n"
        )

        self.progress.set(0)

        self.update_status(
            "Finding Duplicates..."
        )

        self.update()

        try:

            duplicates = find_duplicates(
                folder
            )

        except Exception as error:

            messagebox.showerror(
                "Duplicate Error",
                str(error)
            )

            return

        self.current_duplicates = (
            duplicates
        )

        (
            groups,
            duplicate_files,
            potential_space
        ) = get_duplicate_statistics(
            duplicates
        )

        self.duplicate_groups = groups

        self.duplicate_files = (
            duplicate_files
        )

        self.potential_space = (
            potential_space
        )

        self.duplicates_card.configure(
            text=str(
                duplicate_files
            )
        )

        self.results_box.insert(
            "end",
            f"Duplicate Groups : "
            f"{groups}\n"
        )

        self.results_box.insert(
            "end",
            f"Duplicate Files  : "
            f"{duplicate_files}\n"
        )

        self.results_box.insert(
            "end",
            f"Potential Space  : "
            f"{self.format_size(potential_space)}\n\n"
        )

        if not duplicates:

            self.results_box.insert(
                "end",
                "✅ No duplicate files found."
            )

            self.progress.set(1)

            self.update_status(
                "No Duplicates"
            )

            return

        self.results_box.insert(
            "end",
            "Click '🛡 Review' to safely "
            "choose duplicate files.\n"
        )

        self.progress.set(1)

        self.progress_label.configure(
            text="Duplicate scan complete"
        )

        self.update_status(
            "Duplicates Found"
        )

    # ==========================================
    # REVIEW DUPLICATES
    # ==========================================

    def review_duplicates(self):

        if not self.current_duplicates:

            messagebox.showinfo(
                "No Duplicates",
                "Run 'Find Duplicates' first."
            )

            return

        # --------------------------------------
        # REVIEW WINDOW
        # --------------------------------------

        review_window = ctk.CTkToplevel(
            self
        )

        review_window.title(
            "SmartSort AI - Duplicate Review"
        )

        review_window.geometry(
            "900x650"
        )

        review_window.transient(
            self
        )

        # --------------------------------------
        # TITLE
        # --------------------------------------

        title = ctk.CTkLabel(
            review_window,
            text="🛡 Safe Duplicate Review",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        )

        title.pack(
            pady=(20, 5)
        )

        info = ctk.CTkLabel(
            review_window,
            text=(
                "Review the duplicates below. "
                "SmartSort will keep one copy "
                "and select the additional copies."
            )
        )

        info.pack(
            pady=(0, 15)
        )

        # --------------------------------------
        # SCROLL FRAME
        # --------------------------------------

        scroll_frame = ctk.CTkScrollableFrame(
            review_window
        )

        scroll_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        checkbox_data = []

        group_number = 1

        for file_hash, files in (
            self.current_duplicates.items()
        ):

            group_frame = ctk.CTkFrame(
                scroll_frame,
                corner_radius=10
            )

            group_frame.pack(
                fill="x",
                padx=5,
                pady=8
            )

            group_title = ctk.CTkLabel(
                group_frame,
                text=(
                    f"Duplicate Group "
                    f"{group_number}"
                ),
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            )

            group_title.pack(
                anchor="w",
                padx=15,
                pady=(10, 2)
            )

            hash_label = ctk.CTkLabel(
                group_frame,
                text=(
                    f"SHA-256: "
                    f"{file_hash}"
                ),
                wraplength=800
            )

            hash_label.pack(
                anchor="w",
                padx=15,
                pady=(0, 8)
            )

            for index, file in enumerate(
                files
            ):

                selected = (
                    index != 0
                )

                variable = ctk.BooleanVar(
                    value=selected
                )

                checkbox = ctk.CTkCheckBox(
                    group_frame,
                    text=str(file),
                    variable=variable
                )

                checkbox.pack(
                    anchor="w",
                    padx=20,
                    pady=4
                )

                checkbox_data.append(
                    (
                        variable,
                        Path(file)
                    )
                )

            group_number += 1

        # --------------------------------------
        # BUTTONS
        # --------------------------------------

        button_frame = ctk.CTkFrame(
            review_window,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=15
        )

        cleanup_button = ctk.CTkButton(
            button_frame,
            text="🗑 Move Selected to SmartSort Trash",
            width=300,
            height=45,
            command=lambda: self.perform_cleanup(
                review_window,
                checkbox_data
            )
        )

        cleanup_button.pack(
            side="left",
            padx=8
        )

        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=120,
            height=45,
            command=review_window.destroy
        )

        cancel_button.pack(
            side="left",
            padx=8
        )

    # ==========================================
    # PERFORM CLEANUP
    # ==========================================

    def perform_cleanup(
        self,
        review_window,
        checkbox_data
    ):

        selected_files = [
            path
            for variable, path
            in checkbox_data
            if variable.get()
        ]

        if not selected_files:

            messagebox.showwarning(
                "Nothing Selected",
                "Select at least one duplicate."
            )

            return

        confirmation = messagebox.askyesno(
            "Confirm Safe Cleanup",
            (
                f"{len(selected_files)} files "
                "will be moved to SmartSort Trash.\n\n"
                "They will NOT be permanently deleted.\n\n"
                "You can use Undo to restore them.\n\n"
                "Continue?"
            )
        )

        if not confirmation:
            return

        folder = self.folder_entry.get().strip()

        result = move_to_smart_trash(
            folder,
            selected_files
        )

        records = result["records"]

        if not records:

            messagebox.showerror(
                "Cleanup Failed",
                "No files could be moved."
            )

            return

        self.last_cleanup_session = (
            result["session"]
        )

        review_window.destroy()

        self.results_box.delete(
            "1.0",
            "end"
        )

        self.results_box.insert(
            "end",
            "========== SAFE CLEANUP ==========\n\n"
        )

        self.results_box.insert(
            "end",
            f"🛡 Files moved: "
            f"{len(records)}\n\n"
        )

        self.results_box.insert(
            "end",
            "Files were moved to:\n"
        )

        self.results_box.insert(
            "end",
            f"{result['session']}\n\n"
        )

        self.results_box.insert(
            "end",
            "They were NOT permanently deleted.\n\n"
        )

        self.results_box.insert(
            "end",
            "↩ Click Undo to restore them."
        )

        self.duplicate_files = max(
            0,
            self.duplicate_files -
            len(records)
        )

        self.duplicates_card.configure(
            text=str(
                self.duplicate_files
            )
        )

        self.update_status(
            "Cleanup Complete"
        )

        messagebox.showinfo(
            "Safe Cleanup Complete",
            (
                f"{len(records)} files were moved "
                "to SmartSort Trash.\n\n"
                "Use Undo if you want to restore them."
            )
        )

    # ==========================================
    # UNDO
    # ==========================================

    def undo_last_cleanup(self):

        if not self.last_cleanup_session:

            messagebox.showinfo(
                "Nothing to Undo",
                "There is no cleanup operation "
                "available to undo."
            )

            return

        confirmation = messagebox.askyesno(
            "Undo Cleanup",
            (
                "Restore the files from the "
                "last SmartSort cleanup?"
            )
        )

        if not confirmation:
            return

        restored = undo_cleanup(
            self.last_cleanup_session
        )

        if restored == 0:

            messagebox.showwarning(
                "Undo",
                "No files could be restored."
            )

            return

        self.last_cleanup_session = None

        self.results_box.insert(
            "end",
            "\n\n====================================\n"
        )

        self.results_box.insert(
            "end",
            f"↩ Restored {restored} files."
        )

        self.update_status(
            "Cleanup Restored"
        )

        messagebox.showinfo(
            "Undo Complete",
            f"{restored} files were restored."
        )

        # Re-scan duplicates after restoration

        self.scan_duplicates()

    # ==========================================
    # DASHBOARD
    # ==========================================

    def update_dashboard(self):

        self.files_card.configure(
            text=str(
                self.total_files
            )
        )

        self.categories_card.configure(
            text=str(
                len(self.category_count)
            )
        )

        self.size_card.configure(
            text=self.format_size(
                self.total_size
            )
        )

        self.duplicates_card.configure(
            text=str(
                self.duplicate_files
            )
        )

    # ==========================================
    # STATUS
    # ==========================================

    def update_status(
        self,
        status
    ):

        self.status_card.configure(
            text=status
        )

    # ==========================================
    # FORMAT SIZE
    # ==========================================

    @staticmethod
    def format_size(
        size
    ):

        if size < 1024:

            return f"{size} B"

        if size < 1024 ** 2:

            return (
                f"{size / 1024:.1f} KB"
            )

        if size < 1024 ** 3:

            return (
                f"{size / (1024 ** 2):.1f} MB"
            )

        return (
            f"{size / (1024 ** 3):.1f} GB"
        )


# ==============================================
# START
# ==============================================

if __name__ == "__main__":

    app = SmartSortApp()

    app.mainloop()