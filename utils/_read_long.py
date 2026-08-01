
def _read_long(f):
    '''Read a signed 32-bit integer'''
    return np.int32(struct.unpack('>l', f.read(4))[0])

