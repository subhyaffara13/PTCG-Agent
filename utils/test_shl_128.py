
def test_shl_128():
    with exc_iter(INT128_VALUES) as it:
        for a, in it:
            if a < 0:
                b = -(((-a) << 1) & (2**128 - 1))
            else:
                b = (a << 1) & (2**128 - 1)
            c = mt.extint_shl_128(a)
            if b != c:
                assert_equal(c, b)

