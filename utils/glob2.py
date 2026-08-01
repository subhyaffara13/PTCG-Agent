
def glob2(dirname: StrPath, pattern: str) -> Iterator[str]: ...


def glob2(dirname: BytesPath, pattern: bytes) -> Iterator[bytes]: ...


def glob2(dirname: StrOrBytesPath, pattern: str | bytes) -> Iterator[str | bytes]:
    assert _isrecursive(pattern)
    yield pattern[:0]
    yield from _rlistdir(dirname)

