
def display_path(path: str) -> str:
    """Gives the display value for a given path, making it relative to cwd
    if possible."""
    try:
        relative = Path(path).relative_to(Path.cwd())
    except ValueError:
        # If the path isn't relative to the CWD, leave it alone
        return path
    return os.path.join(".", relative)

