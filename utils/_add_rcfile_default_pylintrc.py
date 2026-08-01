
def _add_rcfile_default_pylintrc(args: list[str]) -> list[str]:
    """Add a default pylintrc with the rcfile option in a list of pylint args."""
    if not any("--rcfile" in arg for arg in args):
        args.insert(0, f"--rcfile={PYLINTRC}")
    return args

