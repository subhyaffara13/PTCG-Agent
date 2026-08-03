import os

def _is_path(name_or_buffer: object) -> TypeIs[str | os.PathLike]:
    return isinstance(name_or_buffer, (str, os.PathLike))

