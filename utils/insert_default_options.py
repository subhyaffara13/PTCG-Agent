
def insert_default_options() -> None:
    """Insert default options to sys.argv."""
    for arg in reversed(get_default_options()):
        sys.argv.insert(1, arg)

