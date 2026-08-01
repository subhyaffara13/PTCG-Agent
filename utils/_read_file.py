
def _read_file(filename):
    with open(filename) as f:
        return f.readlines()


def _read_file(filename: str) -> str:
    with open(filename, "rb") as f:
        b = f.read()
        return b.decode("utf-8")


def _read_file(filepath: bytes | StrPath) -> str:
    with open(filepath, encoding='utf-8') as f:
        return f.read()

