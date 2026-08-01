
def _pop_complete_sse_frame(buffer: str) -> tuple[str | None, str]:
    delimiter_positions = [
        (position, delimiter)
        for delimiter in _SSE_FRAME_DELIMITERS
        if (position := buffer.find(delimiter)) != -1
    ]
    if not delimiter_positions:
        return None, buffer

    position, delimiter = min(delimiter_positions, key=lambda item: item[0])
    frame_end = position + len(delimiter)
    return buffer[:frame_end], buffer[frame_end:]

