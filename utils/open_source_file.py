
def open_source_file(filename: str) -> tuple[TextIOWrapper, str, str]:
    # pylint: disable=consider-using-with
    with open(filename, "rb") as byte_stream:
        encoding = detect_encoding(byte_stream.readline)[0]
    stream = open(filename, newline=None, encoding=encoding)
    data = stream.read()
    return stream, encoding, data

