
def test_complex_parsing(dtype, with_parens):
    s = "(1.0-2.5j),3.75,(7+-5.0j)\n(4),(-19e2j),(0)"
    if not with_parens:
        s = s.replace("(", "").replace(")", "")

    res = np.loadtxt(StringIO(s), dtype=dtype, delimiter=",")
    expected = np.array(
        [[1.0 - 2.5j, 3.75, 7 - 5j], [4.0, -1900j, 0]], dtype=dtype
    )
    assert_equal(res, expected)

