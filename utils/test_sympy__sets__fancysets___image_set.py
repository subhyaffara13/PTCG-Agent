
def test_sympy__sets__fancysets__ImageSet():
    from sympy.sets.fancysets import ImageSet
    from sympy.core.singleton import S
    from sympy.core.symbol import Symbol
    x = Symbol('x')
    assert _test_args(ImageSet(Lambda(x, x**2), S.Naturals))

