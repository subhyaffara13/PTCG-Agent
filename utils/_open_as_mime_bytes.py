
def _open_as_mime_bytes(content: ContentT) -> MimeBytes: ...  # means "if input is not None, output is not None"


def _open_as_mime_bytes(content: Literal[None]) -> Literal[None]: ...  # means "if input is None, output is None"


def _open_as_mime_bytes(content: ContentT | None) -> MimeBytes | None:
    """Open `content` as a binary file, either from a URL, a local path, raw bytes, or a PIL Image.

    Do nothing if `content` is None.
    """
    # If content is None, yield None
    if content is None:
        return None

    # If content is bytes, return it
    if isinstance(content, bytes):
        return MimeBytes(content)

    # If content is raw binary data (bytearray, memoryview)
    if isinstance(content, (bytearray, memoryview)):
        return MimeBytes(bytes(content))

    # If content is a binary file-like object
    if hasattr(content, "read"):  # duck-typing instead of isinstance(content, BinaryIO)
        logger.debug("Reading content from BinaryIO")
        data = content.read()
        mime_type = mimetypes.guess_type(str(content.name))[0] if hasattr(content, "name") else None
        if isinstance(data, str):
            raise TypeError("Expected binary stream (bytes), but got text stream")
        return MimeBytes(data, mime_type=mime_type)

    # If content is a string => must be either a URL or a path
    if isinstance(content, str):
        if content.startswith("https://") or content.startswith("http://"):
            logger.debug(f"Downloading content from {content}")
            response = get_session().get(content)
            mime_type = response.headers.get("Content-Type")
            if mime_type is None:
                mime_type = mimetypes.guess_type(content)[0]
            return MimeBytes(response.content, mime_type=mime_type)

        content = Path(content)
        if not content.exists():
            raise FileNotFoundError(
                f"File not found at {content}. If `data` is a string, it must either be a URL or a path to a local"
                " file. To pass raw content, please encode it as bytes first."
            )

    # If content is a Path => open it
    if isinstance(content, Path):
        logger.debug(f"Opening content from {content}")
        return MimeBytes(content.read_bytes(), mime_type=mimetypes.guess_type(content)[0])

    # If content is a PIL Image => convert to bytes
    if is_pillow_available():
        from PIL import Image

        if isinstance(content, Image.Image):
            logger.debug("Converting PIL Image to bytes")
            buffer = io.BytesIO()
            format = content.format or "PNG"
            content.save(buffer, format=format)
            return MimeBytes(buffer.getvalue(), mime_type=f"image/{format.lower()}")

    # If nothing matched, raise error
    raise TypeError(
        f"Unsupported content type: {type(content)}. "
        "Expected one of: bytes, bytearray, BinaryIO, memoryview, Path, str (URL or file path), or PIL.Image.Image."
    )

