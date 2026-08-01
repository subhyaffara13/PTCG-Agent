
def test_int_byteswap(read_offset, number, int_type, should_byteswap):
    assume(number < 2 ** (8 * int_type(0).itemsize))
    _test(number, int_type, read_offset, should_byteswap)

