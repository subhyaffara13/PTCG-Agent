import os

def _rlistdir(dirname: StrPath) -> Iterator[str]: ...


def _rlistdir(dirname: BytesPath) -> Iterator[bytes]: ...


def _rlistdir(dirname: StrOrBytesPath) -> Iterator[str | bytes]:
    if not dirname:
        if isinstance(dirname, bytes):
            dirname = os.curdir.encode('ASCII')
        else:
            dirname = os.curdir
    try:
        names = os.listdir(dirname)
    except OSError:
        return
    for x in names:
        yield x
        # mypy false-positives: str or bytes type possibility is always kept in sync
        path = os.path.join(dirname, x) if dirname else x  # type: ignore[arg-type]
        for y in _rlistdir(path):
            yield os.path.join(x, y)  # type: ignore[arg-type]

