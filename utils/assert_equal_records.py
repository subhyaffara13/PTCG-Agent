
def assert_equal_records(a, b):
    """
    Asserts that two records are equal.

    Pretty crude for now.

    """
    assert_equal(a.dtype, b.dtype)
    for f in a.dtype.names:
        (af, bf) = (operator.getitem(a, f), operator.getitem(b, f))
        if not (af is masked) and not (bf is masked):
            assert_equal(operator.getitem(a, f), operator.getitem(b, f))

