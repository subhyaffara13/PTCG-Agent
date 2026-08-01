
def test_Lambda_equality():
    assert Lambda((x, y), 2*x) == Lambda((x, y), 2*x)
    # these, of course, should never be equal
    assert Lambda(x, 2*x) != Lambda((x, y), 2*x)
    assert Lambda(x, 2*x) != 2*x
    # But it is tempting to want expressions that differ only
    # in bound symbols to compare the same.  But this is not what
    # Python's `==` is intended to do; two objects that compare
    # as equal means that they are indistibguishable and cache to the
    # same value.  We wouldn't want to expression that are
    # mathematically the same but written in different variables to be
    # interchanged else what is the point of allowing for different
    # variable names?
    assert Lambda(x, 2*x) != Lambda(y, 2*y)

