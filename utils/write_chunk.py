
def write_chunk(outfile, tag, data=strtobytes("")):
    """
    Write a PNG chunk to the output file, including length and
    checksum.
    """

    # http://www.w3.org/TR/PNG/#5Chunk-layout
    outfile.write(struct.pack("!I", len(data)))
    tag = strtobytes(tag)
    outfile.write(tag)
    outfile.write(data)
    checksum = zlib.crc32(tag)
    checksum = zlib.crc32(data, checksum)
    checksum &= 2**32 - 1
    outfile.write(struct.pack("!I", checksum))

