import os

def _create_temp_file(content: bytes):
    """Creates a temporary file with the given content.

    Args:
        content (bytes): The content to write to the file.

    Yields:
        str: The path to the temporary file.
    """
    # Create a temporary file that is readable only by the owner.
    fd, file_path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(content)
        yield file_path
    finally:
        # Securely delete the file after use.
        if os.path.exists(file_path):
            os.remove(file_path)

