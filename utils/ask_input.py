
def ask_input(message: str) -> str:
    """Ask for input interactively."""
    _check_no_input(message)
    return input(message)

