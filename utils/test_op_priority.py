
def test_op_priority():
    from sympy.abc import x
    md = ImmutableDenseNDimArray([1, 2, 3])
    e1 = (1+x)*md
    e2 = md*(1+x)
    assert e1 == ImmutableDenseNDimArray([1+x, 2+2*x, 3+3*x])
    assert e1 == e2

    sd = ImmutableSparseNDimArray([1, 2, 3])
    e3 = (1+x)*sd
    e4 = sd*(1+x)
    assert e3 == ImmutableDenseNDimArray([1+x, 2+2*x, 3+3*x])
    assert e3 == e4

