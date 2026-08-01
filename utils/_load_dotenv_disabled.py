
def _load_dotenv_disabled() -> bool:
    """
    Determine if dotenv loading has been disabled.
    """
    if "PYTHON_DOTENV_DISABLED" not in os.environ:
        return False
    value = os.environ["PYTHON_DOTENV_DISABLED"].casefold()
    return value in {"1", "true", "t", "yes", "y"}

