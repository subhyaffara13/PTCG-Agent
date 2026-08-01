
def remove_readonly(
    func: Callable[..., object],
    path: str,
    excinfo: tuple[type[Exception], Exception, types.TracebackType],
) -> None:
    remove_readonly_exc(func, path, excinfo[1])


def remove_readonly(func, path, exc_info):
    """
    Add support for removing read-only files on Windows.
    """
    _, exc, _ = exc_info
    if func in (os.rmdir, os.remove, os.unlink) and exc.errno == errno.EACCES:
        # change the file to be readable,writable,executable: 0777
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        # retry
        func(path)
    else:
        raise

