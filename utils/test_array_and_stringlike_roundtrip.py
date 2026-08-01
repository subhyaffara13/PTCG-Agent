
def test_array_and_stringlike_roundtrip(strtype):
    """
    Test that string representations of long-double roundtrip both
    for array casting and scalar coercion, see also gh-15608.
    """
    o = 1 + LD_INFO.eps

    if strtype in (np.bytes_, bytes):
        o_str = strtype(str(o).encode("ascii"))
    else:
        o_str = strtype(str(o))

    # Test that `o` is correctly coerced from the string-like
    assert o == np.longdouble(o_str)

    # Test that arrays also roundtrip correctly:
    o_strarr = np.asarray([o] * 3, dtype=strtype)
    assert (o == o_strarr.astype(np.longdouble)).all()

    # And array coercion and casting to string give the same as scalar repr:
    assert (o_strarr == o_str).all()
    assert (np.asarray([o] * 3).astype(strtype) == o_str).all()

