
def test_converter_with_unicode_dtype():
    """
    With the 'bytes' encoding, tokens are encoded prior to being
    passed to the converter. This means that the output of the converter may
    be bytes instead of unicode as expected by `read_rows`.

    This test checks that outputs from the above scenario are properly decoded
    prior to parsing by `read_rows`.
    """
    txt = StringIO('abc,def\nrst,xyz')
    conv = bytes.upper
    res = np.loadtxt(
            txt, dtype=np.dtype("U3"), converters=conv, delimiter=",",
            encoding="bytes")
    expected = np.array([['ABC', 'DEF'], ['RST', 'XYZ']])
    assert_equal(res, expected)

