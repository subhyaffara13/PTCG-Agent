
def _iter_batch_input_entries(file_content: bytes) -> Iterator[dict]:
    """
    Yield parsed batch input JSONL entries one at a time without materializing the
    whole file as a list, so peak memory stays bounded. Raises on a malformed line;
    callers that must survive bad rows should iterate ``_iter_batch_input_lines``
    and parse per-row instead.
    """
    for line in _iter_batch_input_lines(file_content):
        yield json.loads(line)

