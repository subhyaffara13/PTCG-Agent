
def test_safe_binop():
    # Test checked arithmetic routines

    ops = [
        (operator.add, 1),
        (operator.sub, 2),
        (operator.mul, 3)
    ]

    with exc_iter(ops, INT64_VALUES, INT64_VALUES) as it:
        for xop, a, b in it:
            pyop, op = xop
            c = pyop(a, b)

            if not (INT64_MIN <= c <= INT64_MAX):
                assert_raises(OverflowError, mt.extint_safe_binop, a, b, op)
            else:
                d = mt.extint_safe_binop(a, b, op)
                if c != d:
                    # assert_equal is slow
                    assert_equal(d, c)

