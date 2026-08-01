
def decompress(input_file, output_file):
    """Decompress WOFF2 font to OpenType font.

    Args:
            input_file: a file path, file or file-like object (open in binary mode)
                    containing a compressed WOFF2 font.
            output_file: a file path, file or file-like object where to save the
                    decompressed OpenType font.
    """
    log.info("Processing %s => %s" % (input_file, output_file))

    font = TTFont(input_file, recalcBBoxes=False, recalcTimestamp=False)
    font.flavor = None
    font.flavorData = None
    font.save(output_file, reorderTables=True)


def decompress(data):
    (compression,) = struct.unpack(">L", data[4:8])
    scheme = compression >> 27
    size = compression & 0x07FFFFFF
    if scheme == 0:
        pass
    elif scheme == 1 and lz4:
        res = lz4.block.decompress(struct.pack("<L", size) + data[8:])
        if len(res) != size:
            warnings.warn("Table decompression failed.")
        else:
            data = res
    else:
        warnings.warn("Table is compressed with an unsupported compression scheme")
    return (data, scheme)

