
def strftime_now(fmt: str) -> str:
    """
    Custom function for templates that need current date/time formatting (e.g., gpt-oss)

    Args:
        fmt: Format string for datetime.now().strftime()

    Returns:
        Formatted string
    """
    return datetime.now().strftime(fmt)

