
def on_rm_rf_error(
    func: Callable[..., Any] | None,
    path: str,
    excinfo: BaseException
    | tuple[type[BaseException], BaseException, types.TracebackType | None],
    *,
    start_path: Path,
) -> bool:
    """Handle known read-only errors during rmtree.

    The returned value is used only by our own tests.
    """
    if isinstance(excinfo, BaseException):
        exc = excinfo
    else:
        exc = excinfo[1]

    # Another process removed the file in the middle of the "rm_rf" (xdist for example).
    # More context: https://github.com/pytest-dev/pytest/issues/5974#issuecomment-543799018
    if isinstance(exc, FileNotFoundError):
        return False

    if not isinstance(exc, PermissionError):
        warnings.warn(
            PytestWarning(f"(rm_rf) error removing {path}\n{type(exc)}: {exc}")
        )
        return False

    if func not in (os.rmdir, os.remove, os.unlink):
        if func not in (os.open,):
            warnings.warn(
                PytestWarning(
                    f"(rm_rf) unknown function {func} when removing {path}:\n{type(exc)}: {exc}"
                )
            )
        return False

    # Chmod + retry.
    import stat

    def chmod_rw(p: str) -> None:
        mode = os.stat(p).st_mode
        os.chmod(p, mode | stat.S_IRUSR | stat.S_IWUSR)

    # For files, we need to recursively go upwards in the directories to
    # ensure they all are also writable.
    p = Path(path)
    if p.is_file():
        for parent in p.parents:
            chmod_rw(str(parent))
            # Stop when we reach the original path passed to rm_rf.
            if parent == start_path:
                break
    chmod_rw(str(path))

    func(path)
    return True

