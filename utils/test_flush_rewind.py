
def test_flush_rewind():
    stream = BytesIO()
    with make_simple(stream, mode='w') as f:
        f.createDimension('x',4)  # x is used in createVariable
        v = f.createVariable('v', 'i2', ['x'])
        v[:] = 1
        f.flush()
        len_single = len(stream.getvalue())
        f.flush()
        len_double = len(stream.getvalue())

    assert_(len_single == len_double)

