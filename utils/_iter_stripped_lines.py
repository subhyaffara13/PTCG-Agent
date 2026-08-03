from typing import Union

def _iter_stripped_lines(raw_lines: Iterable[Union[str, bytes]]) -> Iterator[str]:
    """Decode (when needed), strip, and drop blank lines from an iterable of lines."""
    for raw in raw_lines:
        line = raw.decode("utf-8") if isinstance(raw, (bytes, bytearray)) else raw
        line = line.strip()
        if line:
            yield line

