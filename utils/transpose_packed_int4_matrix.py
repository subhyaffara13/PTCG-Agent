
def transpose_packed_int4_matrix(packed, rows, cols):
    # unpack to int4 matrix
    total = rows * cols
    high = (packed >> 4) & 0x0F
    low = packed & 0x0F
    int4_vals = np.empty(total, dtype=np.uint8)
    int4_vals[0::2] = low
    int4_vals[1::2] = high
    int4_matrix = int4_vals.reshape((rows, cols))

    # transpose int4 matrix
    int4_matrix_transposed = int4_matrix.T

    # pack to uint8
    flat = int4_matrix_transposed.reshape(-1)
    packed = ((flat[1::2] << 4) & 0xF0) | (flat[0::2] & 0x0F)
    return packed.astype(np.uint8)

