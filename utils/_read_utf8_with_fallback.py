
def _read_utf8_with_fallback(file: str, fallback_encoding=_LOCALE_ENCODING) -> str:
    """See setuptools.unicode_utils._read_utf8_with_fallback"""
    try:
        with open(file, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:  # pragma: no cover
        msg = f"""\
        ********************************************************************************
        `encoding="utf-8"` fails with {file!r}, trying `encoding={fallback_encoding!r}`.

        This fallback behaviour is considered **deprecated** and future versions of
        `setuptools/pkg_resources` may not implement it.

        Please encode {file!r} with "utf-8" to ensure future builds will succeed.

        If this file was produced by `setuptools` itself, cleaning up the cached files
        and re-building/re-installing the package with a newer version of `setuptools`
        (e.g. by updating `build-system.requires` in its `pyproject.toml`)
        might solve the problem.
        ********************************************************************************
        """
        # TODO: Add a deadline?
        #       See comment in setuptools.unicode_utils._Utf8EncodingNeeded
        warnings.warn(msg, PkgResourcesDeprecationWarning, stacklevel=2)
        with open(file, "r", encoding=fallback_encoding) as f:
            return f.read()


def _read_utf8_with_fallback(file: str, fallback_encoding=py39.LOCALE_ENCODING) -> str:
    """
    First try to read the file with UTF-8, if there is an error fallback to a
    different encoding ("locale" by default). Returns the content of the file.
    Also useful when reading files that might have been produced by an older version of
    setuptools.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:  # pragma: no cover
        _Utf8EncodingNeeded.emit(file=file, fallback_encoding=fallback_encoding)
        with open(file, "r", encoding=fallback_encoding) as f:
            return f.read()

