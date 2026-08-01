
def _write_stream(stream, *strings):
    stream.truncate(0)
    stream.seek(0)
    for s in strings:
        stream.write(s)
    stream.seek(0)

