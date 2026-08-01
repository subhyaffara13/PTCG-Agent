
def test_sympy__sets__contains__Contains():
    from sympy.sets.fancysets import Range
    from sympy.sets.contains import Contains
    assert _test_args(Contains(x, Range(0, 10, 2)))

