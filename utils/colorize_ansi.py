
def colorize_ansi(msg: str, msg_style: MessageStyle) -> str:
    """Colorize message by wrapping it with ANSI escape codes."""
    return msg_style._colorize_ansi(msg)

