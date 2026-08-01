
def write_chunks(out, chunks):
    """Create a PNG file by writing out the chunks."""

    out.write(_signature)
    for chunk in chunks:
        write_chunk(out, *chunk)

