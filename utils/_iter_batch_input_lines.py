
def _iter_batch_input_lines(file_content: bytes) -> Iterator[bytes]:
    """
    Yield non-empty JSONL lines (unparsed) one at a time, so a caller can parse
    each row in its own try/except and a single malformed line cannot abort the
    whole pass. Peak memory stays bounded for large batch files.
    """
    start, length, newline = 0, len(file_content), ord("\n")
    while start < length:
        idx = file_content.find(newline, start)
        if idx == -1:
            chunk, start = file_content[start:], length
        else:
            chunk, start = file_content[start:idx], idx + 1
        line = chunk.strip()
        if line:
            yield line

