
def test_sympy__stats__frv__ProductFinitePSpace():
    from sympy.stats.frv import SingleFinitePSpace, ProductFinitePSpace
    from sympy.core.symbol import Symbol
    xp = SingleFinitePSpace(Symbol('x'), die)
    yp = SingleFinitePSpace(Symbol('y'), die)
    assert _test_args(ProductFinitePSpace(xp, yp))

