
def test_bytes():
    assert m.print_bytes(m.return_bytes()) == "bytes[1 0 2 0]"


def test_bytes(doc):
    assert m.bytes_from_char_ssize_t().decode() == "green"
    assert m.bytes_from_char_size_t().decode() == "purple"
    assert m.bytes_from_string().decode() == "foo"
    assert m.bytes_from_str().decode() == "bar"

    assert doc(m.bytes_from_str) == "bytes_from_str() -> bytes"


def test_bytes():
    raw_file = BytesIO()
    f = netcdf_file(raw_file, mode='w')
    # Dataset only has a single variable, dimension and attribute to avoid
    # any ambiguity related to order.
    f.a = 'b'
    f.createDimension('dim', 1)
    var = f.createVariable('var', np.int16, ('dim',))
    var[0] = -9999
    var.c = 'd'
    f.sync()

    actual = raw_file.getvalue()

    expected = (b'CDF\x01'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x0a'
                b'\x00\x00\x00\x01'
                b'\x00\x00\x00\x03'
                b'dim\x00'
                b'\x00\x00\x00\x01'
                b'\x00\x00\x00\x0c'
                b'\x00\x00\x00\x01'
                b'\x00\x00\x00\x01'
                b'a\x00\x00\x00'
                b'\x00\x00\x00\x02'
                b'\x00\x00\x00\x01'
                b'b\x00\x00\x00'
                b'\x00\x00\x00\x0b'
                b'\x00\x00\x00\x01'
                b'\x00\x00\x00\x03'
                b'var\x00'
                b'\x00\x00\x00\x01'
                b'\x00\x00\x00\x00'
                b'\x00\x00\x00\x0c'
                b'\x00\x00\x00\x01'
                b'\x00\x00\x00\x01'
                b'c\x00\x00\x00'
                b'\x00\x00\x00\x02'
                b'\x00\x00\x00\x01'
                b'd\x00\x00\x00'
                b'\x00\x00\x00\x03'
                b'\x00\x00\x00\x04'
                b'\x00\x00\x00\x78'
                b'\xd8\xf1\x80\x01')

    assert_equal(actual, expected)

