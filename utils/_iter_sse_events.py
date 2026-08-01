
def _iter_sse_events(stream: Iterator[str]) -> Iterator[str]:
    """Yield one ``data:`` SSE line at a time from a sync text stream.

    The OCI streaming endpoint does not align SSE event boundaries with HTTP
    read boundaries. A single read may carry multiple events, a single event
    may straddle two reads, and some events arrive separated by only ``\\n``
    instead of ``\\n\\n``. This helper buffers across reads and yields each
    complete ``data:`` line so JSON parsing downstream never sees a partial
    payload.
    """
    buffer = ""
    for item in stream:
        buffer += item
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            stripped = line.strip()
            if stripped.startswith("data:"):
                yield stripped
    stripped = buffer.strip()
    if stripped.startswith("data:"):
        yield stripped

