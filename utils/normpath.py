
def normpath(path: str, options: Options) -> str:
    """Convert path to absolute; but to relative in bazel mode.

    (Bazel's distributed cache doesn't like filesystem metadata to
    end up in output files.)
    """
    # TODO: Could we always use relpath?  (A worry in non-bazel
    # mode would be that a moved file may change its full module
    # name without changing its size, mtime or hash.)
    if options.bazel:
        return os.path.relpath(path)
    else:
        return os.path.abspath(path)


def normpath(filename: StrPath) -> str:
    """Normalize a file/dir name for comparison purposes."""
    return os.path.normcase(os.path.realpath(os.path.normpath(_cygwin_patch(filename))))


def normpath(path: str) -> str:
    normalized = os.path.normpath(path)
    if _WINDOWS_PLATFORM:
        # os.path.normpath converts backslashes to forward slashes on Windows
        # but we want forward slashes, so we convert them back
        normalized = normalized.replace("\\", "/")
    return normalized

