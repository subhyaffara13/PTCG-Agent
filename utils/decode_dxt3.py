
def decode_dxt3(data: bytes) -> tuple[bytearray, bytearray, bytearray, bytearray]:
    """
    input: one "row" of data (i.e. will produce 4*width pixels)
    """

    blocks = len(data) // 16  # number of blocks in row
    ret = (bytearray(), bytearray(), bytearray(), bytearray())

    for block_index in range(blocks):
        idx = block_index * 16
        block = data[idx : idx + 16]
        # Decode next 16-byte block.
        bits = struct.unpack_from("<8B", block)
        color0, color1 = struct.unpack_from("<HH", block, 8)

        (code,) = struct.unpack_from("<I", block, 12)

        r0, g0, b0 = unpack_565(color0)
        r1, g1, b1 = unpack_565(color1)

        for j in range(4):
            high = False  # Do we want the higher bits?
            for i in range(4):
                alphacode_index = (4 * j + i) // 2
                a = bits[alphacode_index]
                if high:
                    high = False
                    a >>= 4
                else:
                    high = True
                    a &= 0xF
                a *= 17  # We get a value between 0 and 15

                color_code = (code >> 2 * (4 * j + i)) & 0x03

                if color_code == 0:
                    r, g, b = r0, g0, b0
                elif color_code == 1:
                    r, g, b = r1, g1, b1
                elif color_code == 2:
                    r = (2 * r0 + r1) // 3
                    g = (2 * g0 + g1) // 3
                    b = (2 * b0 + b1) // 3
                elif color_code == 3:
                    r = (2 * r1 + r0) // 3
                    g = (2 * g1 + g0) // 3
                    b = (2 * b1 + b0) // 3

                ret[j].extend([r, g, b, a])

    return ret

