from typing import Any

def _sanitize_for_log(value: Any) -> str:
    """
    Basic log sanitization helper to reduce log-injection risk.

    Removes newline and carriage-return characters so user-controlled
    values cannot forge additional log lines when written to text logs.
    """
    try:
        text = str(value)
    except Exception:
        # Fallback to repr if str() fails for any reason
        text = repr(value)
    # Strip CR/LF characters commonly used for log injection
    return text.replace("\r", "").replace("\n", "")


def _sanitize_for_log(value: Any) -> str:
    """Strip CR/LF from user-controlled values to prevent log injection."""
    try:
        text = str(value)
    except Exception:
        text = repr(value)
    return text.replace("\r", "").replace("\n", "")

