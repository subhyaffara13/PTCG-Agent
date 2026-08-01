
def test_shr_128():
    with exc_iter(INT128_VALUES) as it:
        for a, in it:
            if a < 0:
                b = -((-a) >> 1)
            else:
                b = a >> 1
            c = mt.extint_shr_128(a)
            if b != c:
                assert_equal(c, b)

