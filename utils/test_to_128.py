
def test_to_128():
    with exc_iter(INT64_VALUES) as it:
        for a, in it:
            b = mt.extint_to_128(a)
            if a != b:
                assert_equal(b, a)

