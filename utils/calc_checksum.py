
def calcChecksum(data):
    """Calculate the checksum for an arbitrary block of data.

    If the data length is not a multiple of four, it assumes
    it is to be padded with null byte.

            >>> print(calcChecksum(b"abcd"))
            1633837924
            >>> print(calcChecksum(b"abcdxyz"))
            3655064932
    """
    remainder = len(data) % 4
    if remainder:
        data += b"\0" * (4 - remainder)
    value = 0
    blockSize = 4096
    assert blockSize % 4 == 0
    for i in range(0, len(data), blockSize):
        block = data[i : i + blockSize]
        longs = struct.unpack(">%dL" % (len(block) // 4), block)
        value = (value + sum(longs)) & 0xFFFFFFFF
    return value

