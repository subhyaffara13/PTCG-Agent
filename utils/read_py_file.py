from typing import Callable

def read_py_file(path: str, read: Callable[[str], bytes]) -> list[str] | None:
    """Try reading a Python file as list of source lines.

    Return None if something goes wrong.
    """
    try:
        source = read(path)
    except OSError:
        return None
    else:
        try:
            source_lines = decode_python_encoding(source).splitlines()
        except DecodeError:
            return None
        return source_lines

