
def test_large_header():
    s = BytesIO()
    d = {'shape': (), 'fortran_order': False, 'descr': '<i8'}
    format.write_array_header_1_0(s, d)

    s = BytesIO()
    d['descr'] = [('x' * 256 * 256, '<i8')]
    assert_raises(ValueError, format.write_array_header_1_0, s, d)

