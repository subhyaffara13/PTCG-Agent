
def _get_prog_name(argv: Sequence[str]) -> str:
    """Determine the CLI program name from the argument vector.

    :param argv: The argument vector (typically ``sys.argv``).
    :returns: ``"python -m pytest"`` when invoked via ``python -m``,
              ``"pytest"`` otherwise.
    """
    argv0 = argv[0] if argv else ""
    if os.path.basename(argv0) == "__main__.py":
        return "python -m pytest"
    return "pytest"

