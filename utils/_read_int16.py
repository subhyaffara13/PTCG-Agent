
def _read_int16(f):
    '''Read a signed 16-bit integer'''
    return np.int16(struct.unpack('>h', f.read(4)[2:4])[0])

