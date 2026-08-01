
def _get_shell_name() -> str | None:
    """Get the current shell name, if available.

    The name will always be lowercase. If the shell cannot be detected, None is
    returned.
    """
    name: str | None  # N.B. shellingham is untyped
    try:
        # N.B. detect_shell returns a tuple of (shell name, shell command).
        # We only need the name.
        name, _cmd = shellingham.detect_shell()  # noqa: TID251
    except shellingham.ShellDetectionFailure:  # pragma: no cover
        name = None

    return name

