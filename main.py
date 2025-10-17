#!/usr/bin/env python3
"""
Virtual Port Manager - Main Application Entry Point
A PyQt6-based GUI wrapper for com0com's setupc.exe command-line tool.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from src.gui.main_window import MainWindow
from src.gui.resources import resource_manager
from src.utils.constants import APP_NAME, APP_VERSION


def main():
    """Initialize and run the Virtual Port Manager application."""
    # Disable dark mode detection
    os.environ['QT_QPA_PLATFORMTHEME'] = ''

    # Create QApplication
    app = QApplication(sys.argv)

    # Force dark color scheme globally (Qt6)
    app.styleHints().setColorScheme(Qt.ColorScheme.Dark)

    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("Virtual Port Manager")

    # Set native Windows style for best integration
    app.setStyle('fusion')

    # Load custom fonts
    poppins_fonts = resource_manager.load_custom_fonts("Poppins")
    jetbrains_fonts = resource_manager.load_custom_fonts("JetBrainsMono")

    if poppins_fonts:
        print(f"Loaded Poppins font variants: {', '.join(poppins_fonts)}")
    else:
        print("Warning: Poppins fonts not loaded, using system fallback")

    if jetbrains_fonts:
        print(f"Loaded JetBrains Mono font variants: {', '.join(jetbrains_fonts)}")
    else:
        print("Warning: JetBrains Mono fonts not loaded, using system fallback")

    # Set application-wide font
    app.setFont(resource_manager.get_app_font())

    # Set Windows-specific attributes for better integration
    if sys.platform == "win32":
        pass  # High DPI support is enabled by default in Qt6

    # Set application icon using resource manager
    app_icon = resource_manager.get_app_icon()
    if not app_icon.isNull():
        app.setWindowIcon(app_icon)

    # Apply Windows theme stylesheet using resource manager
    stylesheet = resource_manager.load_stylesheet("windows_theme.qss")
    if stylesheet:
        app.setStyleSheet(stylesheet)

    # Create and show main window
    main_window = MainWindow()
    main_window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()