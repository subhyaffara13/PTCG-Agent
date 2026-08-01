
def uniform32_from_uint53(x):
    x = np.uint64(x) >> np.uint64(16)
    x = np.uint32(x & np.uint64(0xffffffff))
    return uint32_to_float32(x)

