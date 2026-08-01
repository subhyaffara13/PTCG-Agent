
def is_file_hidden_win(abs_path: str | Path, stat_res: Any | None = None) -> bool:
    """Is a file hidden?

    This only checks the file itself; it should be called in combination with
    checking the directory containing the file.

    Use is_hidden() instead to check the file and its parent directories.

    Parameters
    ----------
    abs_path : unicode
        The absolute path to check.
    stat_res : os.stat_result, optional
        The result of calling stat() on abs_path. If not passed, this function
        will call stat() internally.
    """
    abs_path = Path(abs_path)
    if abs_path.name.startswith("."):
        return True

    if stat_res is None:
        try:
            stat_res = Path(abs_path).stat()
        except OSError as e:
            if e.errno == errno.ENOENT:
                return False
            raise

    try:
        if (
            stat_res.st_file_attributes  # type:ignore[union-attr]
            & stat.FILE_ATTRIBUTE_HIDDEN  # type:ignore[attr-defined]
        ):
            return True
    except AttributeError:
        # allow AttributeError on PyPy for Windows
        # 'stat_result' object has no attribute 'st_file_attributes'
        # https://foss.heptapod.net/pypy/pypy/-/issues/3469
        warnings.warn(
            "hidden files are not detectable on this system, so no file will be marked as hidden.",
            stacklevel=2,
        )

    return False

