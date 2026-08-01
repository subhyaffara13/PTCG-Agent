
def _next_google_genai_sse_chunk(line_iter) -> bytes:
    event_lines: List[str] = []
    while True:
        try:
            line = next(line_iter)
        except StopIteration:
            if event_lines:
                return _encode_google_genai_sse_event(event_lines)
            raise
        if line == "":
            if event_lines:
                return _encode_google_genai_sse_event(event_lines)
            continue
        event_lines.append(line)

