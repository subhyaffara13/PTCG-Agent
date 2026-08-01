
def test_sub_128():
    with exc_iter(INT128_VALUES, INT128_VALUES) as it:
        for a, b in it:
            c = a - b
            if not (INT128_MIN <= c <= INT128_MAX):
                assert_raises(OverflowError, mt.extint_sub_128, a, b)
            else:
                d = mt.extint_sub_128(a, b)
                if c != d:
                    assert_equal(d, c)

