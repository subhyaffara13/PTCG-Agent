
def is_longdouble_binary_compatible():
    try:
        one = np.frombuffer(
            b'\x00\x00\x00\x00\x00\x00\x00\x80\xff\x3f\x00\x00\x00\x00\x00\x00',
            dtype='<f16')
        return one == np.longdouble(1.)
    except TypeError:
        return False

