from pathlib import Path


def extract_file_data(file_data: FileTypes) -> ExtractedFileData:
    """
    Extracts and processes file data from various input formats.

    Args:
        file_data: Can be a tuple of (filename, content, [content_type], [headers]) or direct file content

    Returns:
        ExtractedFileData containing:
        - filename: Name of the file if provided
        - content: The file content in bytes
        - content_type: MIME type of the file
        - headers: Any additional headers
    """
    # Parse the file_data based on its type
    filename = None
    file_content = None
    content_type = None
    file_headers: Mapping[str, str] = {}

    if isinstance(file_data, tuple):
        if len(file_data) == 2:
            filename, file_content = file_data
        elif len(file_data) == 3:
            filename, file_content, content_type = file_data
        elif len(file_data) == 4:
            filename, file_content, content_type, file_headers = file_data
    elif isinstance(file_data, InMemoryFile):
        filename = file_data.name
        file_content = file_data
        content_type = file_data.content_type
    else:
        file_content = file_data
    # Convert content to bytes
    if isinstance(file_content, str):
        # Bare string inputs are rejected: when this helper runs in a proxy
        # request handler the string came from an attacker-controlled form
        # field, and opening it as a path is an arbitrary file read on the
        # proxy host. SDK callers who want to upload from a path should
        # either pass a pathlib.Path (a PathLike instance — see the branch
        # below) or open the file themselves and pass the handle / bytes.
        raise ValueError(
            "extract_file_data does not accept bare str inputs. Pass bytes, "
            "an open file handle, a (filename, content) tuple, or a "
            "pathlib.Path. To upload a local file from a path, call "
            "open(path, 'rb') yourself."
        )
    if isinstance(file_content, PathLike):
        # PathLike (pathlib.Path) is a Python-level type that HTTP form
        # values can't fabricate. Treat as a local file path for SDK
        # convenience.
        if filename is None:
            filename = Path(file_content).name
        with open(file_content, "rb") as f:
            content = f.read()
    elif isinstance(file_content, io.IOBase):
        # If it's a file-like object
        # Try to get filename from file handle if not already set
        if not filename and hasattr(file_content, "name"):
            filename = Path(file_content.name).name

        content = file_content.read()

        if isinstance(content, str):
            content = content.encode("utf-8")
        # Reset file pointer to beginning
        file_content.seek(0)
    elif isinstance(file_content, bytes):
        content = file_content
    else:
        raise ValueError(f"Unsupported file content type: {type(file_content)}")

    # Use provided content type or guess based on filename
    if not content_type:
        if filename:
            guessed_type = mimetypes.guess_type(filename)[0]
            content_type = guessed_type if guessed_type else "application/octet-stream"
        else:
            content_type = "application/octet-stream"

    return ExtractedFileData(
        filename=filename,
        content=content,
        content_type=content_type,
        headers=file_headers,
    )

