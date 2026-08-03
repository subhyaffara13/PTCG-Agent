import os
import sys

def _pager_contextmanager(
    color: bool | None = None,
) -> t.ContextManager[tuple[t.BinaryIO | t.TextIO, str, bool]]:
    """Decide what method to use for paging through text."""
    stdout = _default_text_stdout()

    # There are no standard streams attached to write to. For example,
    # pythonw on Windows.
    if stdout is None:
        stdout = StringIO()

    if not isatty(sys.stdin) or not isatty(stdout):
        return _nullpager(stdout, color)

    # Split using POSIX mode (the default) so that quote characters are
    # stripped from tokens and quoted Windows paths are preserved.
    # Non-POSIX mode retains quotes in tokens, and wrapping tokens
    # with shlex.quote re-introduces quoting issues on Windows.
    pager_cmd_parts = shlex.split(os.environ.get("PAGER", ""))
    if pager_cmd_parts:
        if WIN:
            return _tempfilepager(pager_cmd_parts, color)
        return _pipepager(pager_cmd_parts, color)

    if os.environ.get("TERM") in ("dumb", "emacs"):
        return _nullpager(stdout, color)
    if WIN or sys.platform.startswith("os2"):
        return _tempfilepager(["more"], color)
    return _pipepager(["less"], color)

