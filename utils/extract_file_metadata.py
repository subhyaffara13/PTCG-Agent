from typing import Any, Optional, Tuple
from pathlib import Path


def extract_file_metadata(file_data: FileTypes) -> Tuple[Optional[str], Optional[str]]:
    """
    Resolve (filename, content_type) without reading the file body.

    Mirrors extract_file_data's metadata resolution but never calls .read(), so
    it stays O(1) on large uploads. Use this when only metadata is needed (batch
    detection, GCS object naming) and the body must remain a streamable Path/handle.
    """
    filename: Optional[str] = None
    content_type: Optional[str] = None
    file_content: Any = None

    if isinstance(file_data, tuple):
        if len(file_data) == 2:
            filename, file_content = file_data
        elif len(file_data) == 3:
            filename, file_content, content_type = file_data
        elif len(file_data) == 4:
            filename, file_content, content_type, _ = file_data
    elif isinstance(file_data, InMemoryFile):
        filename = file_data.name
        content_type = file_data.content_type
    else:
        file_content = file_data

    if filename is None:
        if isinstance(file_content, PathLike):
            filename = Path(file_content).name
        elif isinstance(file_content, io.IOBase):
            name_attr = getattr(file_content, "name", None)
            if isinstance(name_attr, str):
                filename = Path(name_attr).name

    if not content_type:
        guessed = mimetypes.guess_type(filename)[0] if filename else None
        content_type = guessed or "application/octet-stream"

    return filename, content_type

