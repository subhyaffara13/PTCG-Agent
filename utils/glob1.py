import os

def glob1(dirname: StrPath, pattern: str) -> list[str]: ...


def glob1(dirname: BytesPath, pattern: bytes) -> list[bytes]: ...


def glob1(dirname: StrOrBytesPath, pattern: str | bytes) -> list[str] | list[bytes]:
    if not dirname:
        if isinstance(pattern, bytes):
            dirname = os.curdir.encode('ASCII')
        else:
            dirname = os.curdir
    try:
        names = os.listdir(dirname)
    except OSError:
        return []
    # mypy false-positives: str or bytes type possibility is always kept in sync
    return fnmatch.filter(names, pattern)  # type: ignore[type-var, return-value]

