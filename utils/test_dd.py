
def test_dd(dd_func, xhi, xlo, expected_yhi, expected_ylo):
    yhi, ylo = dd_func(xhi, xlo)
    assert yhi == expected_yhi, (f"high double ({yhi}) does not equal the "
                                 f"expected value {expected_yhi}")
    assert_allclose(ylo, expected_ylo, rtol=5e-15)

