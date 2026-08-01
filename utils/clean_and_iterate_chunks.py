
def clean_and_iterate_chunks(response):
    buffer = b""

    for chunk in response.iter_content(chunk_size=1024):
        if not chunk:
            break

        buffer += chunk
        while b"\x00" in buffer:
            buffer = buffer.replace(b"\x00", b"")
            yield buffer.decode("utf-8")
            buffer = b""

    # No more data expected, yield any remaining data in the buffer
    if buffer:
        yield buffer.decode("utf-8")

