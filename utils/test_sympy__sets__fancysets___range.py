
def test_sympy__sets__fancysets__Range():
    from sympy.sets.fancysets import Range
    assert _test_args(Range(1, 5, 1))

