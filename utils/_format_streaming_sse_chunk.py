
def _format_streaming_sse_chunk(chunk: Union[str, bytes]) -> Union[str, bytes]:
    if isinstance(chunk, bytes):
        return b"data: " + chunk + b"\n\n"
    return f"data: {chunk}\n\n"

