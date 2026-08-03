from typing import Union
from pathlib import Path


def get_and_replace(
    filename: Path, binary: bool = False, **opts: str
) -> Union[bytes, str]:
    if binary:
        contents = filename.read_bytes()
        return string.Template(contents.decode()).substitute(opts).encode()

    return string.Template(filename.read_text()).substitute(opts)

