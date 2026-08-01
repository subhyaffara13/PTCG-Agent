
def _read_float64(f):
    '''Read a 64-bit float'''
    return np.float64(struct.unpack('>d', f.read(8))[0])

