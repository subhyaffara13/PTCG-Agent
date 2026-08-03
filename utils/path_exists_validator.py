from typing import Any
from pathlib import Path


def path_exists_validator(v: Any) -> Path:
    if not v.exists():
        raise errors.PathNotExistsError(path=v)

    return v

