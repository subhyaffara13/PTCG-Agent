
def test_uint_fill_value_and_filled():
    # See also gh-27269
    a = np.ma.MaskedArray([1, 1], [True, False], dtype="uint16")
    # the fill value should likely not be 99999, but for now guarantee it:
    assert a.fill_value == 999999
    # However, it's type is uint:
    assert a.fill_value.dtype.kind == "u"
    # And this ensures things like filled work:
    np.testing.assert_array_equal(
        a.filled(), np.array([999999, 1]).astype("uint16"), strict=True)

