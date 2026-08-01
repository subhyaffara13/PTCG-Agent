
def _read_float32(f):
    '''Read a 32-bit float'''
    return np.float32(struct.unpack('>f', f.read(4))[0])

