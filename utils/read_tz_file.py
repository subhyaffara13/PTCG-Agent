
def read_tz_file(tar: tarfile.TarFile, name: str) -> bytes:
    start = tar.getnames()[0] + "/"
    inner_file = tar.extractfile(tar.getmember(f"{start}{name}"))
    assert inner_file
    with contextlib.closing(inner_file) as f:
        return f.read()

