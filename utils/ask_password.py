
def ask_password(message: str) -> str:
    """Ask for a password interactively."""
    _check_no_input(message)
    return getpass.getpass(message)

