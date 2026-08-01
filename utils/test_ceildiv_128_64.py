
def test_ceildiv_128_64():
    with exc_iter(INT128_VALUES, INT64_POS_VALUES) as it:
        for a, b in it:
            c = (a + b - 1) // b
            d = mt.extint_ceildiv_128_64(a, b)

            if c != d:
                assert_equal(d, c)

