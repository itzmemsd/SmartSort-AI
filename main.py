"""
SmartSort AI
Intelligent File Organizer

Application entry point.
"""

from app.gui import SmartSortApp


def main():
    """Launch the SmartSort AI GUI."""
    application = SmartSortApp()
    application.mainloop()


if __name__ == "__main__":
    main()