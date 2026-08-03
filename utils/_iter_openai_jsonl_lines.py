from typing import Any

def _iter_openai_jsonl_lines(openai_file_content: FileTypes) -> Iterator[str]:
    """
    Yield non-empty JSONL lines one at a time without materializing the whole
    payload, so peak memory stays bounded regardless of payload size. Mirrors
    ``str.splitlines()`` + ``line.strip()`` for ``\\n`` / ``\\r\\n`` delimited
    JSONL.
    """
    content: Any = openai_file_content
    if isinstance(content, tuple):
        content = content[1]

    if isinstance(content, (bytes, bytearray)):
        # Scan for newlines in place so a large in-memory payload is not copied
        # into a BytesIO just to iterate it line by line.
        newline = ord("\n")
        start, length = 0, len(content)
        while start < length:
            idx = content.find(newline, start)
            if idx == -1:
                chunk, start = content[start:], length
            else:
                chunk, start = content[start:idx], idx + 1
            line = chunk.decode("utf-8").strip()
            if line:
                yield line
        return

    if isinstance(content, str):
        yield from _iter_stripped_lines(io.StringIO(content))
        return

    if isinstance(content, PathLike):
        with open(str(content), "rb") as handle:
            yield from _iter_stripped_lines(handle)
        return

    if hasattr(content, "read"):
        # The handle is read twice per upload (first-row probe for the GCS
        # object name, then the body stream), so it must rewind to 0. A
        # non-seekable handle would silently resume mid-stream and drop the
        # already-consumed first row, so reject it loudly instead.
        seek = getattr(content, "seek", None)
        if seek is None:
            raise ValueError(
                "Batch upload file handle must be seekable; got a non-seekable "
                "stream. Pass bytes, a path, or a seekable handle."
            )
        try:
            seek(0)
        except (OSError, ValueError) as e:
            raise ValueError(
                "Batch upload file handle must be seekable so it can be re-read "
                "for the GCS object name and the upload body."
            ) from e
        yield from _iter_stripped_lines(content)
        return

    raise ValueError("Unsupported file content type")

