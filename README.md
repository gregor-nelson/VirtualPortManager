# com0com Virtual Port Manager

A Windows application for managing com0com virtual serial ports, built with PyQt6. Provides a modern ribbon interface to wrap com0com's setupc.exe command-line tool.

## Features

- **Modern Interface**: Windows 10/11-style ribbon with SVG icons
- **Port Management**: Create, configure, and remove virtual serial port pairs
- **Real-time Output**: Live command execution feedback
- **Driver Operations**: Install, update, reload, and uninstall drivers
- **Parameter Validation**: Comprehensive input validation for all setupc.exe parameters
- **Error Handling**: User-friendly error messages and recovery guidance
- **Settings Persistence**: Saves window geometry, paths, and preferences

## Requirements

**System**
- Windows 10/11
- com0com virtual serial port driver
- Administrator privileges (for driver operations)

**For Users**
1. Download `com0com-gui.exe` from releases
2. Run as administrator (UAC elevation required)
3. Install com0com driver if needed ([download here](https://sourceforge.net/projects/com0com/))
4. Launch the executable directly

## Configuration

Settings are stored in JSON format at:
```
%LOCALAPPDATA%\com0com-gui\config.json
```
**Setup Wizard**
The application includes a first-time setup wizard that:
1. Detects com0com driver installation
2. Locates setupc.exe in common paths
3. Tests setupc.exe functionality
4. Configures initial settings

**Logs**
Error logs stored at: `%LOCALAPPDATA%\com0com-gui\logs\error.log`

## Related Projects

- [com0com](https://sourceforge.net/projects/com0com/) - Virtual serial port driver
- [PyQt6](https://doc.qt.io/qtforpython/) - Python GUI framework
- [setupc.exe Documentation](readme_com0com) - Command reference


**Note**: This application is a GUI wrapper for com0com and requires the com0com driver to be installed separately. com0com is developed and maintained by the com0com project.
