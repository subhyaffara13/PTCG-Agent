
def decode_dxt1(
    data: bytes, alpha: bool = False
) -> tuple[bytearray, bytearray, bytearray, bytearray]:
    """
    input: one "row" of data (i.e. will produce 4*width pixels)
    """

    blocks = len(data) // 8  # number of blocks in row
    ret = (bytearray(), bytearray(), bytearray(), bytearray())

    for block_index in range(blocks):
        # Decode next 8-byte block.
        idx = block_index * 8
        color0, color1, bits = struct.unpack_from("<HHI", data, idx)

        r0, g0, b0 = unpack_565(color0)
        r1, g1, b1 = unpack_565(color1)

        # Decode this block into 4x4 pixels
        # Accumulate the results onto our 4 row accumulators
        for j in range(4):
            for i in range(4):
                # get next control op and generate a pixel

                control = bits & 3
                bits = bits >> 2

                a = 0xFF
                if control == 0:
                    r, g, b = r0, g0, b0
                elif control == 1:
                    r, g, b = r1, g1, b1
                elif control == 2:
                    if color0 > color1:
                        r = (2 * r0 + r1) // 3
                        g = (2 * g0 + g1) // 3
                        b = (2 * b0 + b1) // 3
                    else:
                        r = (r0 + r1) // 2
                        g = (g0 + g1) // 2
                        b = (b0 + b1) // 2
                elif control == 3:
                    if color0 > color1:
                        r = (2 * r1 + r0) // 3
                        g = (2 * g1 + g0) // 3
                        b = (2 * b1 + b0) // 3
                    else:
                        r, g, b, a = 0, 0, 0, 0

                if alpha:
                    ret[j].extend([r, g, b, a])
                else:
                    ret[j].extend([r, g, b])

    return ret

