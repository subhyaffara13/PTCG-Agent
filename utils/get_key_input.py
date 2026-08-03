import sys

def get_key_input():
    """Get a single key input from the user (cross-platform)"""
    try:
        if sys.platform == "win32":
            import msvcrt

            key = msvcrt.getch()
            if key == b"\xe0":  # Arrow keys on Windows
                key = msvcrt.getch()
                if key == b"H":  # Up arrow
                    return "up"
                elif key == b"P":  # Down arrow
                    return "down"
            elif key == b"\r":  # Enter key
                return "enter"
            elif key == b"\x1b":  # Escape key
                return "escape"
            elif key == b"q":
                return "quit"
            return None
        else:
            import termios
            import tty

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                key = sys.stdin.read(1)

                if key == "\x1b":  # Escape sequence
                    key += sys.stdin.read(2)
                    if key == "\x1b[A":  # Up arrow
                        return "up"
                    elif key == "\x1b[B":  # Down arrow
                        return "down"
                    elif key == "\x1b":  # Just escape
                        return "escape"
                elif key == "\r" or key == "\n":  # Enter key
                    return "enter"
                elif key == "q":
                    return "quit"
                return None
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except ImportError:
        # Fallback to simple input if termios/msvcrt not available
        return None

