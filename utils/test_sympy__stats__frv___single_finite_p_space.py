
def test_sympy__stats__frv__SingleFinitePSpace():
    from sympy.stats.frv import SingleFinitePSpace
    from sympy.core.symbol import Symbol

    assert _test_args(SingleFinitePSpace(Symbol('x'), die))

