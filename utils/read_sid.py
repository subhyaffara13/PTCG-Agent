
def readSID(file):
    """Read a String ID (SID) — 2-byte unsigned integer."""
    data = file.read(2)
    if len(data) != 2:
        raise EOFError("Unexpected end of file while reading SID")
    return struct.unpack(">H", data)[0]  # big-endian uint16

