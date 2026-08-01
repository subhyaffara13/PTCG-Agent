
def test_gt_128():
    with exc_iter(INT128_VALUES, INT128_VALUES) as it:
        for a, b in it:
            c = a > b
            d = mt.extint_gt_128(a, b)
            if c != d:
                assert_equal(d, c)

