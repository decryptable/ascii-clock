"""
Repository: https://github.com/decryptable/ascii-clock
Author: decryptable
Description: Real-time ASCII clock rendered from Python source code with adaptive display
"""

import time
import sys
import os
import signal
import inspect
import re
import platform


class Colors:
    """ANSI color codes for terminal output"""

    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    PURPLE = "\033[95m"
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    DARK_GRAY = "\033[2m\033[90m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BG_WHITE = "\033[47m"
    BG_BLACK = "\033[40m"


class Cursor:
    """Terminal cursor manipulation utilities"""

    @staticmethod
    def hide():
        """Hide the terminal cursor"""
        sys.stdout.write("\033[?25l")

    @staticmethod
    def show():
        """Show the terminal cursor"""
        sys.stdout.write("\033[?25h")

    @staticmethod
    def move_to(row, col):
        """Move cursor to specific position"""
        sys.stdout.write(f"\033[{row};{col}H")

    @staticmethod
    def clear_screen():
        """Clear the entire terminal screen"""
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")


class ASCIIClock:
    """Main ASCII clock application class"""

    def __init__(self):
        """Initialize the ASCII clock with default parameters"""
        self.source_code = ""
        self.grid = []
        self.width = 0
        self.height = 0
        self.terminal_resized = True
        self.min_width = 100  # Increased for better spacing
        self.min_height = 25  # Minimum height for proper display
        self.supports_resize_signal = False
        self.os_info = self._get_os_info()

        # Setup signal handler for terminal resize (Unix/Linux/macOS only)
        if hasattr(signal, "SIGWINCH"):
            try:
                signal.signal(signal.SIGWINCH, self._handle_resize)
                self.supports_resize_signal = True
            except (OSError, AttributeError):
                self.supports_resize_signal = False

    def _get_os_info(self):
        """Get operating system information"""
        system = platform.system()
        version = platform.version()
        return {
            "system": system,
            "version": version,
            "is_windows": system == "Windows",
            "is_unix": system in ["Linux", "Darwin", "Unix"],
            "is_mac": system == "Darwin",
        }

    def _handle_resize(self, signum, frame):
        """Handle terminal resize signal (Unix/Linux/macOS only)"""
        self.terminal_resized = True

    def get_minified_source(self):
        """Get the current program's source code in minified form without docstrings"""
        current_file = __file__
        try:
            with open(current_file, "r", encoding="utf-8") as f:
                source = f.read()
        except:
            source = inspect.getsource(sys.modules[__name__])

        # Remove docstrings and comments
        source = self._remove_docstrings_and_comments(source)

        # Minify: remove excessive whitespace
        lines = source.split("\n")
        minified_lines = []

        for line in lines:
            # Strip whitespace
            line = line.strip()
            # Skip empty lines
            if line:
                minified_lines.append(line)

        minified = " ".join(minified_lines)

        # Ensure sufficient length for ASCII art
        while len(minified) < 20000:
            minified += " " + minified

        return minified

    def _remove_docstrings_and_comments(self, source):
        """Remove docstrings and comments from Python source code"""
        # Remove single-line comments
        source = re.sub(r"#.*$", "", source, flags=re.MULTILINE)

        # Remove multi-line docstrings (triple quotes)
        # Pattern to match triple-quoted strings (both """ and ''')
        docstring_pattern = r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\''
        source = re.sub(docstring_pattern, "", source)

        # Remove single-line docstrings
        source = re.sub(r'^\s*""".*?"""\s*$', "", source, flags=re.MULTILINE)
        source = re.sub(r"^\s*\'\'\'.*?\'\'\'\s*$", "", source, flags=re.MULTILINE)

        return source

    def get_terminal_size(self):
        """Get current terminal dimensions with fallback"""
        try:
            if self.os_info["is_windows"]:
                # For Windows, try multiple methods
                try:
                    size = os.get_terminal_size()
                    return size.columns, size.lines
                except:
                    # Fallback for older Windows versions
                    import subprocess

                    result = subprocess.run(
                        ["mode", "con"], capture_output=True, text=True
                    )
                    lines = result.stdout.split("\n")
                    cols, rows = 80, 24
                    for line in lines:
                        if "Columns:" in line:
                            cols = int(line.split(":")[1].strip())
                        elif "Lines:" in line:
                            rows = int(line.split(":")[1].strip())
                    return cols, rows
            else:
                size = os.get_terminal_size()
                return size.columns, size.lines
        except:
            return 80, 24  # Fallback size

    def is_terminal_size_adequate(self):
        """Check if terminal size is adequate for proper display"""
        cols, lines = self.get_terminal_size()
        return cols >= self.min_width and lines >= self.min_height

    def update_display_parameters(self):
        """Update display parameters based on terminal size"""
        cols, lines = self.get_terminal_size()

        # Use full terminal size with minimal padding
        self.width = cols - 2
        self.height = lines - 2

        # Update source code and grid
        self.source_code = self.get_minified_source()
        self.grid = self.create_display_grid()

    def create_display_grid(self):
        """Create display grid filled with source code"""
        grid = []
        char_index = 0

        for row in range(self.height):
            grid_row = []
            for col in range(self.width):
                if char_index < len(self.source_code):
                    grid_row.append(self.source_code[char_index])
                    char_index += 1
                else:
                    char_index = 0
                    grid_row.append(self.source_code[char_index])
            grid.append(grid_row)

        return grid


# Large and clear ASCII patterns (11 height x 9 width) with improved spacing
ASCII_PATTERNS = {
    "0": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "1": [
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "2": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "3": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "4": [
        [1, 1, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1],
    ],
    "5": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "6": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "7": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0],
    ],
    "8": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "9": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    ":": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
}


def get_highlight_positions(time_str, start_row, start_col, grid_width, grid_height):
    """Get positions to highlight for displaying time digits with improved spacing"""
    positions = []
    current_col = start_col

    # Color scheme for different time components
    colors = [
        Colors.RED + Colors.BOLD,  # Hour tens
        Colors.RED + Colors.BOLD,  # Hour units
        Colors.YELLOW + Colors.BOLD,  # Colon
        Colors.GREEN + Colors.BOLD,  # Minute tens
        Colors.GREEN + Colors.BOLD,  # Minute units
        Colors.YELLOW + Colors.BOLD,  # Colon
        Colors.CYAN + Colors.BOLD,  # Second tens
        Colors.CYAN + Colors.BOLD,  # Second units
    ]

    for char_idx, char in enumerate(time_str):
        pattern = ASCII_PATTERNS[char]
        color = colors[char_idx]

        # Process each pixel in the digit pattern
        for row_idx in range(11):  # 11 rows tall
            for col_idx in range(9):  # 9 columns wide
                if pattern[row_idx][col_idx] == 1:
                    highlight_row = start_row + row_idx
                    highlight_col = current_col + col_idx

                    # Ensure within grid bounds
                    if (
                        0 <= highlight_row < grid_height
                        and 0 <= highlight_col < grid_width
                    ):
                        positions.append((highlight_row, highlight_col, color))

        # Increased spacing between characters to prevent overlap
        current_col += 12  # Increased from 11 to 12 for better separation

    return positions


def get_border_positions(time_str, start_row, start_col, grid_width, grid_height):
    """Get positions for border around ASCII art with improved spacing"""
    border_positions = []
    current_col = start_col
    digit_positions = set()

    # First, collect all digit positions
    for char_idx, char in enumerate(time_str):
        pattern = ASCII_PATTERNS[char]
        for row_idx in range(11):
            for col_idx in range(9):
                if pattern[row_idx][col_idx] == 1:
                    digit_row = start_row + row_idx
                    digit_col = current_col + col_idx
                    if 0 <= digit_row < grid_height and 0 <= digit_col < grid_width:
                        digit_positions.add((digit_row, digit_col))
        current_col += 12  # Match the spacing in highlight positions

    # Now find border positions
    current_col = start_col
    for char_idx, char in enumerate(time_str):
        pattern = ASCII_PATTERNS[char]

        # Find border positions around each active pixel
        for row_idx in range(11):
            for col_idx in range(9):
                if pattern[row_idx][col_idx] == 1:
                    center_row = start_row + row_idx
                    center_col = current_col + col_idx

                    # Check surrounding positions for border
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue  # Skip center pixel

                            border_row = center_row + dr
                            border_col = center_col + dc

                            # Check if border position is valid and not a digit pixel
                            if (
                                0 <= border_row < grid_height
                                and 0 <= border_col < grid_width
                                and (border_row, border_col) not in digit_positions
                            ):
                                border_positions.append((border_row, border_col))

        current_col += 12  # Match the spacing

    return list(set(border_positions))  # Remove duplicates


def display_code_with_time(grid, highlight_positions, border_positions):
    """Display grid with highlighting for time and border"""
    highlight_dict = {}
    border_set = set(border_positions)

    # Create dictionary for highlight positions
    for row, col, color in highlight_positions:
        if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
            highlight_dict[(row, col)] = color

    # Display the grid
    for row_idx, row in enumerate(grid):
        line = ""
        for col_idx, char in enumerate(row):
            if (row_idx, col_idx) in highlight_dict:
                # Highlighted digit pixel
                color = highlight_dict[(row_idx, col_idx)]
                line += color + char + Colors.RESET
            elif (row_idx, col_idx) in border_set:
                # Border pixel - lighter color for better separation
                line += Colors.GRAY + char + Colors.RESET
            else:
                # Background source code
                line += Colors.DARK_GRAY + char + Colors.RESET
        print(line)


def display_size_warning(clock):
    """Display warning message when terminal is too small with OS info"""
    Cursor.clear_screen()
    cols, lines = clock.get_terminal_size()

    warning_lines = [
        "",
        "⚠️  TERMINAL TOO SMALL ⚠️",
        "",
        f"Current size: {cols} x {lines}",
        f"Required minimum: {clock.min_width} x {clock.min_height}",
        "",
        "Please resize your terminal window",
        "to view the ASCII clock properly.",
        "",
        "The clock will appear automatically",
        "when the terminal size is adequate.",
        "",
    ]

    # Add OS-specific information
    os_info = [
        f"Operating System: {clock.os_info['system']}",
        "",
    ]

    if not clock.supports_resize_signal:
        os_info.extend(
            [
                "⚠️  Auto-resize detection not supported on this OS",
                "Manual terminal refresh may be needed after resizing",
                "",
            ]
        )

    warning_lines = warning_lines[:5] + os_info + warning_lines[5:]

    # Center the warning message
    start_row = max(1, lines // 2 - len(warning_lines) // 2)

    for i, line in enumerate(warning_lines):
        if start_row + i < lines:
            Cursor.move_to(start_row + i, 1)
            centered_line = line.center(cols)
            if "⚠️" in line and "TERMINAL TOO SMALL" in line:
                print(Colors.YELLOW + Colors.BOLD + centered_line + Colors.RESET)
            elif "Current size:" in line or "Required minimum:" in line:
                print(Colors.RED + centered_line + Colors.RESET)
            elif "Operating System:" in line:
                print(Colors.CYAN + centered_line + Colors.RESET)
            elif "Auto-resize detection" in line or "Manual terminal refresh" in line:
                print(Colors.YELLOW + centered_line + Colors.RESET)
            else:
                print(Colors.WHITE + centered_line + Colors.RESET)


def main():
    """Main application entry point"""
    clock = ASCIIClock()

    try:
        # Setup terminal
        Cursor.hide()

        while True:
            # Check if terminal was resized or first run
            if clock.terminal_resized or not clock.supports_resize_signal:
                clock.update_display_parameters()
                clock.terminal_resized = False

            # Check if terminal size is adequate
            if not clock.is_terminal_size_adequate():
                display_size_warning(clock)
                time.sleep(1)
                continue

            # Calculate center position for time display with improved spacing
            time_width = (
                8 * 12 - 3
            )  # 8 characters * 12 spacing - 3 for better centering
            time_start_row = max(1, clock.height // 2 - 5)
            time_start_col = max(5, (clock.width - time_width) // 2)

            # Get current time
            current_time = time.strftime("%H:%M:%S")

            # Get highlight and border positions
            highlight_positions = get_highlight_positions(
                current_time, time_start_row, time_start_col, clock.width, clock.height
            )

            border_positions = get_border_positions(
                current_time, time_start_row, time_start_col, clock.width, clock.height
            )

            # Clear screen and display
            Cursor.clear_screen()
            display_code_with_time(clock.grid, highlight_positions, border_positions)

            # Wait for next update
            time.sleep(1)

    except KeyboardInterrupt:
        Cursor.clear_screen()
        sys.exit(0)

    except Exception as e:
        Cursor.show()
        Cursor.clear_screen()
        print(f"Error: {e}")
        print(f"OS: {clock.os_info['system']}")
        print("Please check terminal compatibility and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
