
def _fix_utf16_32_line_stream(steam: Iterable[bytes], codec: str) -> Iterable[bytes]:
    r"""Handle line ending for UTF16 and UTF32 correctly.

    Currently, Python simply strips the required zeros after \n after the
    line ending. Leading to lines that can't be decoded properly
    """
    if not codec.startswith("utf-16") and not codec.startswith("utf-32"):
        yield from steam
    else:
        # First we get all the bytes in memory
        content = b"".join(line for line in steam)

        new_line = _cached_encode_search("\n", codec)

        # Now we split the line by the real new line in the correct encoding
        # we can't use split as it would strip the \n that we need
        start = 0
        while True:
            pos = content.find(new_line, start)
            if pos >= 0:
                yield content[start : pos + len(new_line)]
            else:
                # Yield the rest and finish
                if content[start:]:
                    yield content[start:]
                break

            start = pos + len(new_line)

