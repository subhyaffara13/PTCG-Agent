
def test_neg_128():
    with exc_iter(INT128_VALUES) as it:
        for a, in it:
            b = -a
            c = mt.extint_neg_128(a)
            if b != c:
                assert_equal(c, b)

