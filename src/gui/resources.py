"""
Resource Management for VirtualPortManager GUI
Handles theme loading, icon management, asset paths, and custom font loading.
"""

import sys
from pathlib import Path
from typing import Optional, Dict, List
from PyQt6.QtGui import QIcon, QPixmap, QFont, QFontDatabase
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt


class ResourceManager:
    """Centralized resource management for GUI assets."""

    def __init__(self):
        self._base_path = self._get_base_path()
        self._assets_path = self._base_path / "assets"
        self._styles_path = self._assets_path / "styles"
        self._icons_path = self._assets_path / "icons"
        self._fonts_path = self._assets_path / "fonts"

        # Font configuration
        self._default_font_family = "Poppins"  # Easy to change
        self._default_font_size = 9
        self._loaded_fonts: Dict[str, int] = {}  # font_name -> font_id

        # Ensure directories exist
        self._styles_path.mkdir(parents=True, exist_ok=True)

    def _get_base_path(self) -> Path:
        """Get the base path of the application."""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable - PyInstaller sets sys._MEIPASS
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller temp extraction folder
                return Path(sys._MEIPASS)
            else:
                # Fallback to executable directory
                return Path(sys.executable).parent
        else:
            # Running as script - go up from src/gui/resources.py to project root
            return Path(__file__).parent.parent.parent

    def get_stylesheet_path(self, stylesheet_name: str = "windows_theme.qss") -> Optional[Path]:
        """Get path to stylesheet file."""
        stylesheet_path = self._styles_path / stylesheet_name
        if stylesheet_path.exists():
            return stylesheet_path
        return None

    def load_stylesheet(self, stylesheet_name: str = "windows_theme.qss") -> str:
        """Load stylesheet content."""
        stylesheet_path = self.get_stylesheet_path(stylesheet_name)
        if stylesheet_path and stylesheet_path.exists():
            try:
                with open(stylesheet_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Warning: Failed to load stylesheet {stylesheet_name}: {e}")
                return ""
        else:
            print(f"Warning: Stylesheet file not found: {stylesheet_name}")
            return ""

    def get_icon_path(self, icon_name: str, subfolder: str = "") -> Optional[Path]:
        """Get path to icon file."""
        if subfolder:
            icon_path = self._icons_path / subfolder / icon_name
        else:
            icon_path = self._icons_path / icon_name

        if icon_path.exists():
            return icon_path
        return None

    def load_icon(self, icon_name: str, subfolder: str = "") -> QIcon:
        """Load icon from assets."""
        icon_path = self.get_icon_path(icon_name, subfolder)
        if icon_path:
            return QIcon(str(icon_path))
        else:
            print(f"Warning: Icon not found: {icon_name}")
            return QIcon()  # Return empty icon as fallback

    def load_pixmap(self, icon_name: str, subfolder: str = "") -> QPixmap:
        """Load pixmap from assets."""
        icon_path = self.get_icon_path(icon_name, subfolder)
        if icon_path:
            return QPixmap(str(icon_path))
        else:
            print(f"Warning: Pixmap not found: {icon_name}")
            return QPixmap()  # Return empty pixmap as fallback

    def get_app_icon(self) -> QIcon:
        """Get the main application icon."""
        # Try ICO first, then SVG as fallback
        ico_icon = self.load_icon("app_icon.ico")
        if not ico_icon.isNull():
            return ico_icon

        svg_icon = self.load_icon("app_icon.svg")
        if not svg_icon.isNull():
            return svg_icon

        return QIcon()  # Empty icon if neither found

    @property
    def assets_path(self) -> Path:
        """Get assets directory path."""
        return self._assets_path

    @property
    def icons_path(self) -> Path:
        """Get icons directory path."""
        return self._icons_path

    @property
    def styles_path(self) -> Path:
        """Get styles directory path."""
        return self._styles_path

    @property
    def fonts_path(self) -> Path:
        """Get fonts directory path."""
        return self._fonts_path

    # ========== FONT MANAGEMENT ==========

    def load_custom_fonts(self, font_folder: str = "Poppins") -> List[str]:
        """
        Load all custom fonts from a specific font folder.

        Args:
            font_folder: Name of subfolder in assets/fonts (default: "Poppins")

        Returns:
            List of successfully loaded font family names.
        """
        loaded_families = []

        font_dir = self._fonts_path / font_folder

        if not font_dir.exists():
            print(f"Warning: Font directory not found: {font_dir}")
            return loaded_families

        # Find all .ttf and .otf files
        font_files = list(font_dir.glob("*.ttf")) + list(font_dir.glob("*.otf"))

        if not font_files:
            print(f"Warning: No font files found in {font_dir}")
            return loaded_families

        # Load each font file
        for font_file in font_files:
            font_id = QFontDatabase.addApplicationFont(str(font_file))

            if font_id != -1:
                # Get font families from this file
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    family_name = families[0]
                    self._loaded_fonts[family_name] = font_id
                    if family_name not in loaded_families:
                        loaded_families.append(family_name)
            else:
                print(f"Warning: Failed to load font: {font_file.name}")

        if loaded_families:
            print(f"Loaded {len(font_files)} font files ({', '.join(loaded_families)})")

        return loaded_families

    def get_app_font(self, size: Optional[int] = None, weight: Optional[QFont.Weight] = None) -> QFont:
        """
        Get the application font with optional size and weight.

        Args:
            size: Font size in points (uses default if None)
            weight: QFont.Weight enum value (Normal, Medium, DemiBold, Bold, etc.)

        Returns:
            QFont configured with the custom font family
        """
        font_size = size if size is not None else self._default_font_size
        font = QFont(self._default_font_family, font_size)

        if weight is not None:
            font.setWeight(weight)

        return font

    def get_monospace_font(self, size: Optional[int] = None) -> QFont:
        """
        Get the monospace font (JetBrains Mono) for numeric displays and logs.

        Args:
            size: Font size in points (uses default if None)

        Returns:
            QFont configured with JetBrains Mono and fallback chain
        """
        font_size = size if size is not None else self._default_font_size
        font = QFont("JetBrains Mono", font_size)
        font.setStyleHint(QFont.StyleHint.TypeWriter)
        font.setFamilies(["JetBrains Mono", "Cascadia Code", "Cascadia Mono", "Consolas", "Courier New", "monospace"])
        return font

    def set_default_font_family(self, family: str):
        """Change the default font family. Call before loading fonts."""
        self._default_font_family = family

    def set_default_font_size(self, size: int):
        """Change the default font size."""
        self._default_font_size = size

    def is_font_loaded(self, family: str) -> bool:
        """Check if a font family has been loaded."""
        return family in self._loaded_fonts

    def get_loaded_fonts(self) -> List[str]:
        """Get list of all loaded font families."""
        return list(self._loaded_fonts.keys())


# Global resource manager instance
resource_manager = ResourceManager()
