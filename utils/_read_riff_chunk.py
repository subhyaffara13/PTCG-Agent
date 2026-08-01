
def _read_riff_chunk(fid):
    str1 = fid.read(4)  # File signature
    if str1 == b'RIFF':
        is_rf64 = False
        is_big_endian = False
        fmt = '<I'
    elif str1 == b'RIFX':
        is_rf64 = False
        is_big_endian = True
        fmt = '>I'
    elif str1 == b'RF64':
        is_rf64 = True
        is_big_endian = False
        fmt = '<Q'
    else:
        # There are also .wav files with "FFIR" or "XFIR" signatures?
        raise ValueError(f"File format {repr(str1)} not understood. Only "
                         "'RIFF', 'RIFX', and 'RF64' supported.")
    # Size of entire file
    if not is_rf64:
        file_size = struct.unpack(fmt, fid.read(4))[0] + 8
        rf64_chunk_size = None
        str2 = fid.read(4)
    else:
        # Skip 0xFFFFFFFF (-1) bytes
        fid.read(4)
        str2 = fid.read(4)
        str3 = fid.read(4)
        if str3 != b'ds64':
            raise ValueError("Invalid RF64 file: ds64 chunk not found.")
        ds64_size = struct.unpack("<I", fid.read(4))[0]
        file_size = struct.unpack(fmt, fid.read(8))[0] + 8
        rf64_chunk_size = struct.unpack('<Q', fid.read(8))[0]
        # Ignore additional attributes of ds64 chunk like sample count, tables, etc.
        # and just skip to the next chunk
        fid.seek(ds64_size - 16, 1)

    if str2 != b'WAVE':
        raise ValueError(f"Not a WAV file. RIFF form type is {repr(str2)}.")

    return file_size, is_big_endian, is_rf64, rf64_chunk_size

