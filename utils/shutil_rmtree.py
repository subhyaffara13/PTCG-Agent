
def shutil_rmtree(
    path: StrOrBytesPath,
    ignore_errors: bool = False,
    onexc: _OnExcCallback | None = None,
) -> None:
    if sys.version_info >= (3, 12):
        return shutil.rmtree(path, ignore_errors, onexc=onexc)

    def _handler(fn: Callable[..., Any], path: str, excinfo: ExcInfo) -> None:
        if onexc:
            onexc(fn, path, excinfo[1])

    return shutil.rmtree(path, ignore_errors, onerror=_handler)

