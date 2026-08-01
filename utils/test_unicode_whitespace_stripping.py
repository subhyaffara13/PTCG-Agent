
def test_unicode_whitespace_stripping(dtype):
    # Test that all numeric types (and bool) strip whitespace correctly
    # \u202F is a narrow no-break space, `\n` is just a whitespace if quoted.
    # Currently, skip float128 as it did not always support this and has no
    # "custom" parsing:
    txt = StringIO(' 3 ,"\u202F2\n"')
    res = np.loadtxt(txt, dtype=dtype, delimiter=",", quotechar='"')
    assert_array_equal(res, np.array([3, 2]).astype(dtype))

