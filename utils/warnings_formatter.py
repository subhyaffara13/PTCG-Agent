
def warnings_formatter(
    message, category=UserWarning, filename="", lineno=-1, line=""
):
    """Monkey patch for warnings.warn to suppress cruft output."""
    return f"{message}\n"

