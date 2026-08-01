
def pack_bytes_to_4bit(src_8bit: bytes) -> bytearray:
    """
    Copies a source array of 8-bit values into a destination bytearray of packed 4-bit values.
    Assumes that the source values are already in the appropriate int4 range.
    :parameter src_8bit: The 8-bit element values to pack.
    :return A bytearray with every two 8-bit src elements packed into a single byte.
    """
    num_elems = len(src_8bit)
    if num_elems == 0:
        return bytearray()

    dst_size = (num_elems + 1) // 2  # Ex: 5 8-bit elems packed into 3 bytes
    dst = bytearray(dst_size)

    src_i: int = 0
    dst_i: int = 0

    # Pack two 8-bit elements into a single byte in each iteration.
    while src_i < num_elems - 1:
        dst[dst_i] = ((src_8bit[src_i + 1] & 0xF) << 4) | (src_8bit[src_i] & 0xF)
        dst_i += 1
        src_i += 2

    if src_i < num_elems:
        # Odd number of elements.
        dst[dst_i] = src_8bit[src_i] & 0xF

    return dst

